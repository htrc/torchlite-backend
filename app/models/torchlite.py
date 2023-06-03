from typing import Any
from pydantic import BaseModel
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
        self._disabled_volumes: list = []
        self.volumes: list[Volume] | None = None

        if self.ef_id:
            ef_workset = EFApi().workset(self.ef_id)
            if ef_workset:
                self.volumes = [Volume(htid) for htid in ef_workset.htids]

    def __repr__(self) -> str:
        return f"Workset(name={self.name}, id={self.id[-11:]})"

    def disable_volume(self, htid: str) -> None:
        if self.volumes:
            try:
                vol = [v for v in self.volumes if v.htid == htid][0]
            except IndexError:
                vol = None

            if vol:
                self._disabled_volumes.append(vol)
                self.volumes = [v for v in self.volumes if v.htid != htid]

    def enable_volume(self, htid: str) -> None:
        if self.volumes:
            try:
                vol = [v for v in self._disabled_volumes if v.htid == htid][0]
            except IndexError:
                vol = None

            if vol:
                self.volumes.append(vol)
                self._disabled_volumes = [v for v in self._disabled_volumes if v.htid != htid]

    @property
    def metadata(self):
        return [v.metadata for v in self.volumes]


class Volume(TorchliteObject):
    def __init__(self, htid: str) -> None:
        super().__init__()
        self.htid: str = htid
        self._metadata: ef.VolumeMetadata | None = None
        self._features: ef.EF | None = None
        self._tokens: TokenCounter | None = None

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

    @property
    def tokens(self) -> TokenCounter:
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


class Dashboard(TorchliteObject):
    def __init__(self, name: str | None = None) -> None:
        super().__init__()
        self.name = name
        self.workset: Workset | None = None

    def __repr__(self) -> str:
        return f"Dashboard(name={self.name}, id={self.id[-11:]})"


class Widget(TorchliteObject):
    def __init__(self, name: str | None = None) -> None:
        super().__init__()
        self._widget_class = "generic"
        self.workset: Workset | None = None
        self._data: list | None = None

    def __repr__(self) -> str:
        return f"Widget(class={self._widget_class}, id={self.id[-11:]})"


class TimelineWidget(Widget):
    def __init__(self, name: str | None = None) -> None:
        super().__init__()
        self._widget_class = "timeline"

    @property
    def data(self) -> list[Any] | None:
        if self._data is None:
            if self.workset and self.workset.volumes:
                self._data = [{"htid": vol.htid, "pubDate": vol.metadata.pubDate} for vol in self.workset.volumes]
        return self._data


class Projector(TorchliteObject):
    def __init__(self, name: str | None = None) -> None:
        super().__init__()
        self.name = name
        self.workset: Workset | None = None

    def __repr__(self) -> str:
        return f"Projector(name={self.name}, id={self.id[-11:]})"
