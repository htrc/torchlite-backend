# -*- coding: utf-8 -*-
from typing import List, Optional

import htrc.ef.datamodels as ef
from htrc.ef.api import Api


class Volume:
    def __init__(self, data: ef.Volume) -> None:
        self.data: ef.Volume = data
        self.htid = self.data.htid

    def __repr__(self) -> str:
        return f"Torchlite_Volume({self.htid})"


class Workset:
    """
    Torchlite Workset

    This class encapsulates data about a workset.  It includes raw
    data retrieved from the HTRC ef-api, as well as user
    customizations and modifications.
    """

    def __init__(self, wsid: str, ef_api: Api) -> None:
        self._ef_api: Api = ef_api
        self.id: str = wsid
        self._ef_workset: Optional[ef.Workset] = self._ef_api.get_workset(wsid)
        self._volumes: Optional[List[Volume]] = None

    def __repr__(self) -> str:
        return f"Torchlite_Workset({self.id})"

    @property
    def volumes(self) -> Optional[List[Volume]]:
        if self._volumes is None:
            ef_volumes = self._ef_api.get_workset_volumes(self.id)
            if ef_volumes:
                self._volumes = [Volume(v) for v in ef_volumes]
        return self._volumes

    def metadata(self, fields: Optional[List[str]] = None) -> List[ef.Volume] | None:
        return self._ef_api.get_workset_metadata(self.id, fields)

    @property
    def htids(self) -> List[str] | None:
        if self._ef_workset:
            return self._ef_workset.htids
        else:
            return None
