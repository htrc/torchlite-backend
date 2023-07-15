from typing import Any
from rdflib import Graph, Namespace
from SPARQLWrapper import SPARQLWrapper, JSON
from app.models.torchlite import Workset

# mypy: ignore-errors


def wd_id_of(viaf_id):
    SDO = Namespace("http://schema.org/")
    WDE = Namespace("http://www.wikidata.org/entity/")
    url = f"{viaf_id}/rdf.xml"
    g = Graph()
    try:
        g.parse(url)
    except Exception:
        return None

    try:
        u = list(
            filter(
                lambda x: x.startswith(WDE),
                g.objects(subject=None, predicate=SDO.sameAs),
            )
        )[0]
    except Exception:
        return None

    return str(u)


def wikidata_data(wikidata_id: str):
    endpoint = "https://query.wikidata.org/sparql"

    query_template = """select ?pob ?pobLabel ?coord ?dob
    where
    {{ <{subject}> wdt:P19 ?pob .
    <{subject}> wdt:P569 ?dob .
    ?pob wdt:P625 ?coord .
    SERVICE wikibase:label {{ bd:serviceParam wikibase:language "en". }}
    }}"""

    query = query_template.format(subject=wikidata_id)
    sparql: SPARQLWrapper = SPARQLWrapper(endpoint)
    sparql.setReturnFormat(JSON)
    sparql.setQuery(query)

    try:
        results: Any = sparql.queryAndConvert()
        if results and results["results"]["bindings"]:
            bindings: dict = results["results"]["bindings"][0]
    except Exception:
        return None
    data: dict = {
        "pob": bindings["pob"]["value"],
        "pobLabel": bindings["pobLabel"]["value"],
        "coordinates": bindings["coord"]["value"],
        "dob": bindings["dob"]["value"],
    }

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
        clist = flatten([v.metadata.contributor for v in metadata if v.metadata.contributor is not None])
        return list(filter(lambda x: x.type == "http://id.loc.gov/ontologies/bibframe/Person", clist))

    def data(self):
        if self._data is None:
            viaf_ids = (c.id for c in self.contributors)
            wd_ids = (wd_id_of(id) for id in viaf_ids if id is not None)
            self._data = (wikidata_data(id) for id in wd_ids if id is not None)

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
