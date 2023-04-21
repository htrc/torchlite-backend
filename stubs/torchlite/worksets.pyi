import htrc.ef.datamodels as ef
from _typeshed import Incomplete
from htrc.ef.api import Api as Api
from typing import List, Union

class Workset:
    id: Incomplete
    def __init__(self, wsid: str, ef_api: Api) -> None: ...
    @property
    def volumes(self): ...
    def metadata(self, fields: Union[List[str], None] = ...) -> List[ef.Volume]: ...
    @property
    def htids(self): ...

class Volume:
    data: Incomplete
    htid: Incomplete
    def __init__(self, data: ef.Volume) -> None: ...
