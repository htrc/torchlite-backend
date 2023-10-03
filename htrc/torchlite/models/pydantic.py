from typing import TypeVar, Type

import sqlalchemy.types as types
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy import Dialect, JSON
from sqlalchemy.dialects.postgresql import JSONB

T = TypeVar("T", bound=Type[BaseModel])


class PydanticType(types.TypeDecorator):
    impl = types.JSON
    cache_ok = True

    def __init__(self, pydantic_type: T):
        super().__init__()
        self.pydantic_type = pydantic_type

    def load_dialect_impl(self, dialect):
        # Use JSONB for PostgreSQL and JSON for other databases.
        if dialect.name == "postgresql":
            return dialect.type_descriptor(JSONB())
        else:
            return dialect.type_descriptor(JSON())

    def coerce_compared_value(self, op, value):
        return self.impl.coerce_compared_value(op, value)

    def process_bind_param(self, value: T, dialect: Dialect):
        return jsonable_encoder(value) if value else None

    def process_result_value(self, value: T, dialect: Dialect):
        return self.pydantic_type.model_validate(value) if value else None
