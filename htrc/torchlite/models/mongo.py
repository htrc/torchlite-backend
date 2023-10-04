import os
import uuid
from datetime import datetime

from pydantic import BaseModel, BaseConfig


class PyUuid(uuid.UUID):
    def __init__(self, s: str | None = None):
        if not s:
            super().__init__(bytes=os.urandom(16), version=4)
        else:
            super().__init__(s)

    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        return v if isinstance(v, uuid.UUID) else uuid.UUID(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")


class MongoModel(BaseModel):
    class Config(BaseConfig):
        allow_population_by_field_name = True
        json_encoders = {
            datetime: lambda dt: dt.isoformat(),
            uuid.UUID: str,
        }

    @classmethod
    def __from_mongo(cls, data: dict):
        if not data:
            return data
        id = data.pop('_id', None)
        return cls(**dict(data, id=id))

    @classmethod
    async def from_mongo(cls, coro):
        data = await coro
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

        parsed = self.dict(
            exclude_unset=exclude_unset,
            exclude_defaults=exclude_defaults,
            by_alias=by_alias,
            **kwargs,
        )

        # Mongo uses `_id` as default key. We should stick to that as well.
        if '_id' not in parsed and 'id' in parsed:
            parsed['_id'] = parsed.pop('id')

        return parsed
