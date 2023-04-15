import urllib.parse
from typing import List, Union
from pydantic import NoneStr
import requests
import htrc.ef.datamodels as ef

# function cleanId(id) {
#   const i = id.indexOf('.');
#   if (i == -1) throw `Invalid clean htid: ${id}`;
#   const lib = id.substring(0, i);
#   const libId = id.substring(i+1);
#   return `${lib}.${libId.replaceAll(':', '+').replaceAll('/', '=').replaceAll('.', ',')}`;
# }


def cleanId(id):
    lib, libId = id.split('.')
    cleaned = libId.translate(str.maketrans(":/.", "+=,"))
    return f"{lib}.{cleaned}"


class Api:
    base_uri: str = "https://tools.htrc.illinois.edu/ef-api"
    worksets_uri: str = f"{base_uri}/worksets"
    volumes_uri: str = f"{base_uri}/volumes"

    def get(self, uri):
        r = requests.get(uri)
        r.raise_for_status()
        return r.json()['data']

    def get_workset(self, wsid: str) -> ef.Workset:
        uri = f"{self.worksets_uri}/{wsid}"
        return ef.Workset(**self.get(uri))

    def get_workset_volumes(self, wsid: str, *fields) -> List[ef.Volume]:
        uri = f"{self.worksets_uri}/{wsid}/volumes"
        if fields:
            uri = f"{uri}?fields={','.join(fields)}"
        data = self.get(uri)
        return [ef.Volume(**item) for item in data]

    def get_volume_data(
        self,
        htid: str,
        pos: Union[bool, None] = None,
        fields: Union[List[str], None] = None,
    ) -> dict:
        uri = f"{self.volumes_uri}/{cleanId(htid)}"
        queries = {}
        if pos is not None:
            queries['pos'] = f"{str(pos).lower()}"
        if fields:
            queries['fields'] = ','.join(fields)

        if queries:
            uri = f"{uri}?{urllib.parse.urlencode(queries)}"
        return self.get(uri)

    def get_volume_metadata(
        self, htid: str, fields: Union[List[str], None] = None
    ) -> dict:
        uri = f"{self.volumes_uri}/{cleanId(htid)}/metadata"
        queries = {}
        if fields:
            queries['fields'] = ','.join(fields)

        if queries:
            uri = f"{uri}?{urllib.parse.urlencode(queries)}"
        return self.get(uri)

    def get_pages(self, htid: str, seq: List[int], pos: bool, **fields):
        pass
