from collections import namedtuple
from SPARQLWrapper import SPARQLWrapper, JSON
import requests
from rdflib import Graph, Namespace
from app.services.ef_api import EFApi
from app.models.torchlite import Workset, Volume


def wd_id_of(viaf_id):
    SDO = Namespace("http://schema.org/")
    WDE = Namespace("http://www.wikidata.org/entity/")
    url = f"{viaf_id}/rdf.xml"
    g = Graph()
    try:
        g.parse(url)
    except:
        return None

    try:
        u = list(
            filter(
                lambda x: x.startswith(WDE),
                g.objects(subject=None, predicate=SDO.sameAs),
            )
        )[0]
    except:
        return None

    return str(u)


def wikidata_data(wikidata_id: str):
    endpoint = "https://query.wikidata.org/sparql"

    query_template = """select ?country ?countryLabel ?coord ?code ?dob
    where
    {{ <{subject}> wdt:P27 ?country .
    <{subject}> wdt:P569 ?dob .
    ?country wdt:P625 ?coord .
    OPTIONAL {{ ?country wdt:P299 ?code }}
    SERVICE wikibase:label {{ bd:serviceParam wikibase:language "en". }}
    }}"""

    query = query_template.format(subject=wikidata_id)
    sparql: SPARQLWrapper = SPARQLWrapper(endpoint)
    sparql.setReturnFormat(JSON)
    sparql.setQuery(query)

    try:
        results = sparql.queryAndConvert()
        bindings = results['results']['bindings'][0]
    except:
        return None
    data = {
        "coordinates": bindings['coord']['value'],
        "dob": bindings['dob']['value'],
    }
    if "code" in bindings:
        data["countryiso"] = bindings['code']['value']

    return data


def map_data(viaf_id):
    wikidata_id = wd_id_of(viaf_id)
    return wikidata_data(wikidata_id)


def flatten(a_list):
    result = []
    for item in a_list:
        if isinstance(item, list):
            result = result + flatten(item)
        else:
            result.append(item)
    return result


class Widget:
    pass


class MapWidget(Widget):
    def __init__(self, workset: Workset) -> None:
        self.workset: Workset = workset
        self._data = None

    @property
    def contributors(self):
        metadata = self.workset.metadata(["htid", "metadata.contributor"])
        clist = flatten([v.metadata.contributor for v in metadata if v.metadata.contributor != None])
        return list(filter(lambda x: x.type == 'http://id.loc.gov/ontologies/bibframe/Person', clist))

    def data(self):
        if self._data is None:
            viaf_ids = (c.id for c in self.contributors)
            wd_ids = (wd_id_of(id) for id in viaf_ids if id != None)
            self._data = (wikidata_data(id) for id in wd_ids if id != None)

        return self._data


class TimelineWidget(Widget):
    def __init__(self, workset: Workset) -> None:
        self.workset: Workset = workset
        self._data = None

    def data(self):
        if self._data is None:
            metadata = self.workset.metadata(["htid", "metadata.pubDate"])
            self._data = [{"id": v.htid, "pubdate": v.metadata.pubDate} for v in metadata]
        return self._data
