import httpx
import models
from typing import List, Optional

from htrc.torchlite.config import config


def clean_id(id: str) -> str:
    """
    Converts a HTID into a "clean" version that can be used as a filename

    :param id: The HTID to convert
    :return: The "clean" version that can be used as a filename
    """
    lib, lib_id = id.split(".")
    cleaned = lib_id.translate(str.maketrans(":/.", "+=,"))
    return f"{lib}.{cleaned}"


class EfApi:
    def __init__(self, ef_api_url: str = config.EF_API_URL):
        self.ef_api_url = ef_api_url
    #
    # def get(self, uri: str) -> dict | None:
    #     r: requests.models.Response = requests.get(uri)
    #     r.raise_for_status()
    #     r.json()
    #     try:
    #         return r.json()["data"]
    #     except KeyError:
    #         return None
    #
    # async def get_workset(self, wsid: str) -> models.Workset:
    #     uri: str = f"{self.ef_api_url}/worksets/{wsid}"
    #     response = self.get(uri)
    #     if response:
    #         return ef.Workset(**response)
    #     else:
    #         return None
    #
    # def get_workset_metadata(self, wsid: str, fields: Optional[List[str]]) -> List[ef.Volume] | None:
    #     uri = f"{self.worksets_uri}/{wsid}/metadata"
    #     queries: dict = {}
    #     if fields:
    #         queries["fields"] = ",".join(fields)
    #
    #     if queries:
    #         uri = f"{uri}?{urllib.parse.urlencode(queries)}"
    #
    #     data: dict | None = self.get(uri)
    #     if data:
    #         return [ef.Volume(**item) for item in data]
    #     else:
    #         return None
    #
    # def get_workset_volumes(self, wsid: str, fields: Optional[List[str]] = None) -> List[ef.Volume] | None:
    #     uri: str = f"{self.worksets_uri}/{wsid}/volumes"
    #     if fields:
    #         uri = f"{uri}?fields={','.join(fields)}"
    #     data: dict | None = self.get(uri)
    #     if data:
    #         return [ef.Volume(**item) for item in data]
    #     else:
    #         return None
    #
    # def get_volume_data(
    #     self, htid: str, pos: Optional[bool] = None, fields: Optional[List[str]] = None
    # ) -> List[ef.Volume] | None:
    #     uri: str = f"{self.volumes_uri}/{clean_id(htid)}"
    #     queries: dict = {}
    #     if pos is not None:
    #         queries["pos"] = f"{str(pos).lower()}"
    #     if fields:
    #         queries["fields"] = ",".join(fields)
    #     if queries:
    #         uri = f"{uri}?{urllib.parse.urlencode(queries)}"
    #     data: dict | None = self.get(uri)
    #     if data:
    #         return [ef.Volume(**item) for item in data]
    #     else:
    #         return None
    #
    # def get_volume_metadata(self, htid: str, fields: Optional[List[str]]) -> List[ef.Volume] | None:
    #     uri: str = f"{self.volumes_uri}/{clean_id(htid)}/metadata"
    #     queries: dict = {}
    #     if fields:
    #         queries["fields"] = ",".join(fields)
    #     if queries:
    #         uri = f"{uri}?{urllib.parse.urlencode(queries)}"
    #     data: dict | None = self.get(uri)
    #     if data:
    #         return [ef.Volume(**item) for item in data]
    #     else:
    #         return None
    #
    # def get_pages(
    #     self,
    #     htid: str,
    #     seq: Optional[List[str]],
    #     pos: Optional[bool] = None,
    #     fields: Optional[List[str]] = None,
    # ) -> List[ef.Volume] | None:
    #     uri: str = f"{self.volumes_uri}/{clean_id(htid)}/pages"
    #     queries: dict = {}
    #     if seq is not None:
    #         queries["seq"] = ",".join(seq)
    #     if pos is not None:
    #         queries["pos"] = f"{str(pos).lower()}"
    #     if fields:
    #         queries["fields"] = ",".join(fields)
    #
    #     if queries:
    #         uri = f"{uri}?{urllib.parse.urlencode(queries)}"
    #     data: dict | None = self.get(uri)
    #     if data:
    #         return [ef.Volume(**item) for item in data]
    #     else:
    #         return None
