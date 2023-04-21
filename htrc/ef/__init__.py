import requests

from htrc.ef.datamodels import Workset, Volume


class EndPoint:
    base_uri = "https://tools.htrc.illinois.edu/ef-api"

    def get(self, uri):
        r = requests.get(uri)
        r.raise_for_status()
        return r.json()["data"]


class WorksetEndPoint(EndPoint):
    def __init__(self) -> None:
        super().__init__()
        self.base_uri = f"{self.base_uri}/worksets"

    def get_workset(self, wsid: str) -> Workset:
        uri = f"{self.base_uri}/{wsid}"
        return Workset(**self.get(uri))

    def get_volumes(self, wsid):
        uri = f"{self.base_uri}/{wsid}/volumes"
        return [Volume(**item) for item in self.get(uri)]

    def get_metadata(self, wsid, *fields):
        uri = f"{self.base_uri}/{wsid}/metadata"
        if fields:
            uri = f"{uri}?fields={','.join(fields)}"

        self.get(uri)
        # return data
        return [Volume(**item) for item in self.get(uri)]

    def post(self, uri, data):
        r = requests.post(uri, data=data)
        return r

    def create_workset(self, volume_ids):
        data = " ".join(volume_ids)
        requests.post(self.base_uri, data=data, headers={"Content-Type": "text/plain"})
        return data


class VolumeEndPoint(EndPoint):
    def __init__(self) -> None:
        super().__init__()
        self.base_uri = f"{self.base_uri}/volumes"
