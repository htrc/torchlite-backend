# -*- coding: utf-8 -*-
from typing import List, Union

import htrc.ef.datamodels as ef
from htrc.ef.api import Api



class Volume:
    def __init__(self, data: ef.Volume) -> None:
        self.data: ef.Volume = data
        self.htid = self.data.htid

    def __repr__(self) -> str:
        return f"Torchlite_Volume({self.htid})"

class Workset:
    """Torchlite Workset

    This class encapsulates data about a workset.  It includes raw
    data retrieved from the HTRC ef-api, as well as user
    customizations and modifications.

    """

    def __init__(self, wsid: str, ef_api: Api) -> None:
        self._ef_api: Api = ef_api
        self.id: str = wsid
        self._ef_workset: ef.Workset = self._ef_api.get_workset(wsid)
        self._volumes: Union[List[Volume], None] = None

    def __repr__(self) -> str:
        return f"Torchlite_Workset({self.id})"

    @property
    def volumes(self) -> Union[List[Volume], None]:
        if self._volumes is None:
            self._volumes = [Volume(v) for v in self._ef_api.get_workset_volumes(self.id)]
        return self._volumes

    def metadata(self, fields: Union[List[str], None] = None) -> List[ef.Volume]:
        return self._ef_api.get_workset_metadata(self.id, fields)

    @property
    def htids(self) -> List[str]:
        return self._ef_workset.htids
