from pydantic import BaseModel
from uuid import uuid4
from app.services.ef_api import EFApi
import app.models.ef as ef
from app.models.tokens import tokenPosCount, Token


class TorchliteObject:
    def __init__(self) -> None:
        self.id = str(uuid4())


class Workset(TorchliteObject):
    def __init__(self, ef_wsid: str | None = None) -> None:
        super().__init__()
        self.ef_id: str | None = None
        self.volumes: list[Volume] = []

        if ef_wsid:
            ef_workset: ef.Workset | None = EFApi().workset(ef_wsid)
            if ef_workset:
                self.ef_id = ef_workset.id
                self.volumes = [Volume(htid) for htid in ef_workset.htids]

    def __repr__(self) -> str:
        return f"Workset({self.id[-11:]})"

    @property
    def metadata(self):
        return [v.metadata for v in self.volumes]


class Volume(TorchliteObject):
    def __init__(self, htid: str) -> None:
        super().__init__()
        self.htid: str = htid
        self._metadata: ef.VolumeMetadata | None = None
        self._features: ef.EF | None = None

    def __repr__(self) -> str:
        return f"Volume({self.htid})"

    @property
    def metadata(self):
        if self._metadata is None:
            self._metadata = EFApi().volume_metadata(self.htid)
        return self._metadata

    @property
    def features(self):
        if self._features is None:
            self._features = EFApi().volume_features(self.htid)
        return self._features


class Page(TorchliteObject):
    def __init__(self, vol_id: str, page_features: ef.PageFeatures) -> None:
        super().__init__()
        self.vol_id = vol_id
        self.features: ef.PageFeatures = page_features
        self._tokens: list | None = None

    def __repr__(self) -> str:
        return f"Page({self.features.seq})"

    @property
    def tokens(self) -> list[Token]:
        if self._tokens is None:
            self._tokens = tokenPosCount(self.features.body.tokenPosCount)
        return self._tokens
