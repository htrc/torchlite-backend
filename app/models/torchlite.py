from typing import Optional
from uuid import uuid4
from app.services.ef_api import EFApi
import app.models.ef as ef
from app.models.tokens import TokenCounter


class TorchliteObject:
    def __init__(self) -> None:
        self.id = str(uuid4())


class Workset(TorchliteObject):
    def __init__(self, ef_wsid: str | None = None, name: str | None = None, description: str | None = None) -> None:
        super().__init__()
        self.name: str | None = name
        self.description: str | None = description
        self.ef_id: str | None = ef_wsid
        self.volumes: list[Volume] | None = None

        if self.ef_id:
            ef_workset = EFApi().workset(self.ef_id)
            if ef_workset:
                self.volumes = [Volume(htid) for htid in ef_workset.htids]

    def __repr__(self) -> str:
        return f"Workset(name={self.name}, id={self.id[-11:]})"

    def add_volume(self, htid: str) -> None:
        if self.volumes:
            found = [v for v in self.volumes if v.htid == htid]
            if not found:
                self.volumes.append(Volume(htid))
        else:
            self.volumes = [Volume(htid)]

    def remove_volume(self, htid: str) -> None:
        if self.volumes:
            remainder = [v for v in self.volumes if v.htid != htid]
            self.volumes = remainder

    def metadata(self, fields: list | None = None) -> list | None:
        if self.ef_id:
            return EFApi().workset_metadata(self.ef_id, fields)
        else:
            return None


class Volume(TorchliteObject):
    def __init__(self, htid: str) -> None:
        super().__init__()
        self.htid: str = htid
        self._metadata: ef.VolumeMetadata | None = None
        self._features: Optional[ef.VolumeFeatures] = None
        self._tokens: TokenCounter | None = None

    def __repr__(self) -> str:
        return f"Volume({self.htid})"

    @property
    def metadata(self) -> ef.VolumeMetadata | None:
        if self._metadata is None:
            self._metadata = EFApi().volume_metadata(self.htid)
        return self._metadata

    @property
    def features(self) -> ef.VolumeFeatures | None:
        if self._features is None:
            self._features = EFApi().volume_features(self.htid)
        return self._features

    @property
    def tokens(self) -> TokenCounter | None:
        if self._tokens is None:
            self._tokens = EFApi().tokens(self.htid)
        return self._tokens


class Page(TorchliteObject):
    def __init__(self, vol_id: str, page_features: ef.PageFeatures) -> None:
        super().__init__()
        self.vol_id = vol_id
        self.features: ef.PageFeatures = page_features
        self._tokens: list | None = None

    def __repr__(self) -> str:
        return f"Page({self.features.seq})"
