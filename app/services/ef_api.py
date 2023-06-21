from typing import List, Optional
import requests
from requests.models import Response
import app.models.ef as ef
import app.models.tokens as tokens


def clean_id(id: str) -> str:
    """
    Converts a HTID into a "clean" version that can be used as a filename

    :param id: The HTID to convert
    :return: The "clean" version that can be used as a filename
    """
    lib, lib_id = id.split(".", 1)
    cleaned = lib_id.translate(str.maketrans(":/.", "+=,"))
    return f"{lib}.{cleaned}"


class EFApi:
    base_uri: str = "https://tools.htrc.illinois.edu/ef-api"
    worksets_uri: str = f"{base_uri}/worksets"
    volumes_uri: str = f"{base_uri}/volumes"

    def get(self, uri: str, params: dict = {}) -> dict | None:
        headers = {"Accept": "application/json"}
        if params:
            r: Response = requests.get(uri, headers=headers, params=params)
        else:
            r = requests.get(uri, headers=headers)

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

    # def workset_metadata(self, wsid: str) -> List[ef.VolumeMetadata] | None:
    #     uri = f"{self.worksets_uri}/{wsid}/metadata"
    #     response = self.get(uri)
    #     if response:
    #         return [ef.VolumeMetadata(**item) for item in response]
    #     else:
    #         return None

    def workset_metadata(self, wsid: str, fields: Optional[List[str]]) -> List[ef.Volume] | None:
        uri = f"{self.worksets_uri}/{wsid}/metadata"
        params: dict = {}
        if fields:
            params["fields"] = ",".join(fields)

        response: dict | None = self.get(uri, params=params)
        if response:
            return [ef.Volume(**item) for item in response]
        else:
            return None

    def workset_metadata_subfields(self, wsid: str, fields: Optional[List[str]]) -> List[ef.Volume] | None:
        uri = f"{self.worksets_uri}/{wsid}/metadata"
        params: dict = {}
        if fields:
            params["fields"] = ",".join(fields)

        response: dict | None = self.get(uri, params=params)
        if response:
            return [ef.Volume(**item) for item in response]
        else:
            return None

    def volume_metadata(self, htid: str) -> ef.VolumeMetadata | None:
        uri: str = f"{self.volumes_uri}/{clean_id(htid)}/metadata"

        data: dict | None = self.get(uri)
        if data:
            return ef.VolumeMetadata(**data["metadata"])
        else:
            return None

    def volume_features(self, htid: str) -> ef.VolumeFeatures | None:
        uri: str = f"{self.volumes_uri}/{clean_id(htid)}"
        data: dict | None = self.get(uri)
        if data:
            volume: ef.EF = ef.EF(**data)
            return volume.features
        else:
            return None

    def volume_features_subfields(
        self, htid: str, pos: Optional[bool] = None, fields: Optional[List[str]] = None
    ) -> ef.EF | None:
        uri: str = f"{self.volumes_uri}/{clean_id(htid)}"
        params: dict = {}
        match pos:
            case True:
                params["pos"] = "true"
            case False:
                params["pos"] = "false"

        if fields:
            params["fields"] = ",".join(fields)

        data: dict | None = self.get(uri, params=params)

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

    def tokens(self, htid: str):
        uri: str = f"{self.volumes_uri}/{clean_id(htid)}"
        params = {"pos": "false", "fields": "features.pages.body.tokensCount"}
        data: dict | None = self.get(uri, params=params)
        if data:
            pages = data['features']['pages']
            token_counter: tokens.TokenCounter = tokens.TokenCounter()
            for page in pages:
                tokensCount = page['body']['tokensCount']
                if tokensCount:
                    for tc in tokens.tokensCount(tokensCount):
                        token_counter.add(tc)
            return token_counter
        else:
            return None

    def tokens_old(self, htid: str, sections: list[str] = ["body"]) -> set:
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
