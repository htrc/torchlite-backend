from abc import abstractmethod
from typing import Any

from pydantic import model_serializer

from ..models.base import BaseModel


class WidgetBase(BaseModel):
    @model_serializer(mode='wrap')
    def serialize_model(self, handler) -> dict[str, Any]:
        result = handler(self)
        result.update({'type': getattr(self, 'type')})
        return result

    @abstractmethod
    def get_data(self) -> Any:
        raise NotImplementedError
