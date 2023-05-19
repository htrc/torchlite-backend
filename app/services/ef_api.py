import urllib.parse
from typing import List, Optional
import requests
import app.schemas.ef as ef


def clean_id(id: str) -> str:
    """
    Converts a HTID into a "clean" version that can be used as a filename

    :param id: The HTID to convert
    :return: The "clean" version that can be used as a filename
    """
    lib, lib_id = id.split(".")
    cleaned = lib_id.translate(str.maketrans(":/.", "+=,"))
    return f"{lib}.{cleaned}"


class EFApi:
    base_uri: str = "https://tools.htrc.illinois.edu/ef-api"
    worksets_uri: str = f"{base_uri}/worksets"
    volumes_uri: str = f"{base_uri}/volumes"

    def get(self, uri: str) -> dict | None:
        headers = {"Accept": "application/json"}
        r: requests.models.Response = requests.get(uri, headers=headers)
        r.raise_for_status()
        try:
            return r.json()["data"]
        except KeyError:
            return None

    def workset(self, wsid: str) -> ef.Workset | None:
        uri: str = f"{self.worksets_uri}/{wsid}"
        response = self.get(uri)
        if response:
            return ef.Workset(**response)
        else:
            return None

    def workset_metadata(self, wsid: str) -> List[ef.VolumeMetadata] | None:
        uri = f"{self.worksets_uri}/{wsid}/metadata"
        response = self.get(uri)
        if response:
            return [ef.VolumeMetadata(**item) for item in response]
        else:
            return None

    def volume_metadata(self, htid: str) -> ef.VolumeMetadata | None:
        uri: str = f"{self.volumes_uri}/{clean_id(htid)}/metadata"

        data: dict | None = self.get(uri)
        if data:
            return ef.VolumeMetadata(**data["metadata"])
        else:
            return None

    def volume_features(self, htid: str) -> ef.EF | None:
        uri: str = f"{self.volumes_uri}/{clean_id(htid)}"
        data: dict | None = self.get(uri)
        if data:
            return ef.EF(**data)
        else:
            return None

    def volume_features_subfields(
        self, htid: str, pos: Optional[bool] = None, fields: Optional[List[str]] = None
    ) -> ef.EF | None:
        uri: str = f"{self.volumes_uri}/{clean_id(htid)}"
        queries: dict = {}
        if pos is not None:
            queries["pos"] = f"{str(pos).lower()}"
        if fields:
            queries["fields"] = ",".join(fields)

        if queries:
            uri = f"{uri}?{urllib.parse.urlencode(queries)}"

        data: dict | None = self.get(uri)
        if data:
            return ef.EF(**data)
        else:
            return None

    def pages(self, htid: str):
        uri: str = f"{self.volumes_uri}/{clean_id(htid)}/pages"
        data: dict | None = self.get(uri)
        if data:
            return [ef.PageFeatures(**page) for page in data["pages"]]
        else:
            return None

    def tokens(self, htid: str, sections: list[str] = ["body"]) -> set:
        token_set: set = set()
        pages = self.pages(htid)
        if pages:
            for page in pages:
                for section_name in sections:
                    section = page.dict()[section_name]
                    if section and "tokenPosCount" in section.keys():
                        section_toks: set = {tok for tok in section["tokenPosCount"].keys()}
                        token_set = token_set | section_toks
        return token_set
