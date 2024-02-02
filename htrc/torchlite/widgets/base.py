from abc import abstractmethod
from enum import IntEnum
from typing import Any

from pydantic import model_serializer

from ..errors import WidgetImplementationError
from ..models.base import BaseModel
from ..models.workset import WorksetInfo


class WidgetDataTypes(IntEnum):
    metadata_only = 1
    vols_no_pos = 2
    vols_with_pos = 3


class WidgetBase(BaseModel):

    def __init__(self, /, **data: Any) -> None:
        super().__init__(**data)
        if not hasattr(self, 'type'):
            raise WidgetImplementationError(f"Widget 'type' not defined for {self.__class__.__name__}")
        if not hasattr(self, 'data_type'):
            raise WidgetImplementationError(f"Widget 'data_type' not defined for {self.__class__.__name__}")

    @model_serializer(mode='wrap')
    def serialize_model(self, handler) -> dict[str, Any]:
        result = handler(self)
        result.update({'type': getattr(self, 'type')})
        return result

    @abstractmethod
    async def get_data(self, workset_info: WorksetInfo) -> Any:
        raise NotImplementedError
