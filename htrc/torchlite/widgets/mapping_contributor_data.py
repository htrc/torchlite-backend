import asyncio
import random
from datetime import datetime
from typing import Literal, Final, Pattern, AnyStr

import httpx
import regex as re
from pydantic import AnyHttpUrl

from .base import WidgetBase
from ..ef import models as ef_models
from ..http_client import http
from ..models.base import BaseModel
from ..utils import make_list, make_batches, flatten, parse_dict


class WikidataEntry(BaseModel):
    item: str
    country_iso: str
    city: str
    latitude: float
    longitude: float
    year_of_birth: int | None


class MappingContributorDataWidget(WidgetBase):
    type: Literal['MappingContributorData'] = 'MappingContributorData'
    min_year: int | None = None
    max_year: int | None = None

    BATCH_SIZE: Final[int] = 50
    WIKIDATA_URL: Final[str] = 'https://query.wikidata.org/sparql'
    SPARQL_QUERY_TEMPLATE: Final[str] = '''
        SELECT ?item ?countryiso ?cityCoords ?cityLabel ?dob
        WHERE {{
            VALUES ?item {{ {values} }}
            ?person wdtn:P214 ?item .
            ?person p:P19 ?pob_entry .
            ?pob_entry ps:P19 ?pob .
            ?pob_entry a wikibase:BestRank .
            OPTIONAL {{
                ?pob p:P17/ps:P17/wdt:P299 ?countryiso .
            }}
            OPTIONAL {{
                ?pob wdt:P625 ?cityCoords ;
                rdfs:label ?cityLabel . 
                FILTER(lang(?cityLabel) = 'en') .
            }}
            OPTIONAL {{
                ?person p:P569 ?dob_entry . 
                ?dob_entry ps:P569 ?dob .
                ?dob_entry a wikibase:BestRank .
            }}
        }}
    '''
    POINT_RE: Final[Pattern[AnyStr]] = re.compile(r'Point\((?P<longitude>\S+) (?P<latitude>\S+)\)')

    @classmethod
    def get_contributor_ids(cls, volumes: list[ef_models.Volume]) -> list[AnyHttpUrl]:
        contributor_ids = list({
            contributor.id
            for v in volumes
            for contributor in make_list(v.metadata.contributor)
            if contributor.type == 'http://id.loc.gov/ontologies/bibframe/Person'
        })

        return contributor_ids

    @classmethod
    def try_parse_date(cls, s: str | None) -> datetime | None:
        if not s:
            return None

        try:
            return datetime.strptime(s, '%Y-%m-%dT%H:%M:%SZ')
        except ValueError:
            return None

    @classmethod
    async def query_wikidata(
            cls, viaf_ids: list[str], http: httpx.AsyncClient, delay_sec: float = 0
    ) -> list[WikidataEntry] | None:
        values = ' '.join(f'<{viaf_id}>' for viaf_id in viaf_ids)
        query = cls.SPARQL_QUERY_TEMPLATE.format(values=values)

        if delay_sec:
            await asyncio.sleep(delay_sec)

        data = await http.get(
            cls.WIKIDATA_URL,
            params={'query': query},
            headers={'Accept': 'application/sparql-results+json'}
        )
        data = data.json()

        if parse_dict(data, 'results.bindings'):
            entries = []
            for bindings in data['results']['bindings']:
                item = parse_dict(bindings, 'item.value')
                dob = cls.try_parse_date(parse_dict(bindings, 'dob.value'))
                country_iso = parse_dict(bindings, 'countryiso.value')
                city = parse_dict(bindings, 'cityLabel.value')
                city_coords = parse_dict(bindings, 'cityCoords.value')

                entry = {
                    'item': item,
                    'year_of_birth': dob.year if dob else None,
                    'country_iso': country_iso,
                    'city': city,
                    **(cls.POINT_RE.match(city_coords).groupdict() if city_coords else {})
                }
                entries.append(WikidataEntry(**entry))
        else:
            entries = None

        return entries

    async def get_data(self, volumes: list[ef_models.Volume]) -> list[WikidataEntry]:
        contributor_ids = self.get_contributor_ids(volumes)
        contributor_ids = [c_id.replace('www.', '') for c_id in contributor_ids if 'viaf.org' in c_id]
        req_batches = make_batches(contributor_ids, self.BATCH_SIZE)

        def delay():
            return (100 * random.randint(0, len(req_batches))) / 1000  # seconds

        data = await asyncio.gather(*[self.query_wikidata(batch, http, delay_sec=delay()) for batch in req_batches])

        return flatten(data)
