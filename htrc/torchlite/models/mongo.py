import uuid
from datetime import datetime
from typing import Annotated, Any

from pydantic import ConfigDict, AfterValidator, WithJsonSchema

from .base import BaseModel


def validate_object_id(v: Any) -> uuid.UUID:
    if isinstance(v, uuid.UUID):
        return v
    return uuid.UUID(v)


PyUuid = Annotated[
    str | uuid.UUID,
    AfterValidator(validate_object_id),
    WithJsonSchema({"type": "string"}, mode="serialization"),
]


class MongoModel(BaseModel):
    model_config = ConfigDict(
        **BaseModel.model_config,
        json_encoders={
            datetime: lambda dt: dt.isoformat(),
            uuid.UUID: str,
        },
    )

    @classmethod
    def __from_mongo(cls, data: dict):
        if not data:
            return data
        id = data.pop('_id', None)
        return cls(**dict(data, id=id))

    @classmethod
    async def from_mongo(cls, coro):
        data = await coro
        if data is None:
            return None
        if isinstance(data, list):
            return [cls.__from_mongo(d) for d in data]
        elif isinstance(data, dict):
            return cls.__from_mongo(data)
        else:
            raise ValueError(f"Unsupported data type: {type(data)}")

    def to_mongo(self, **kwargs):
        exclude_unset = kwargs.pop('exclude_unset', True)
        exclude_defaults = kwargs.pop('exclude_defaults', True)
        by_alias = kwargs.pop('by_alias', True)

        parsed = self.model_dump(
            exclude_unset=exclude_unset,
            exclude_defaults=exclude_defaults,
            by_alias=by_alias,
            **kwargs,
        )

        # Mongo uses `_id` as default key. We should stick to that as well.
        if '_id' not in parsed and 'id' in parsed:
            parsed['_id'] = parsed.pop('id')

        return parsed
