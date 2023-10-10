from typing import Any

from pydantic import BaseModel as PydanticBaseModel
from pydantic.alias_generators import to_camel


class BaseModel(PydanticBaseModel, alias_generator=to_camel, populate_by_name=True):
    ...
