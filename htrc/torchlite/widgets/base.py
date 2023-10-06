from abc import ABC, abstractmethod
from typing import Any


class WidgetBase(ABC):
    @abstractmethod
    def get_data(self) -> Any:
        raise NotImplementedError
