from pydantic import BaseModel
from uuid import uuid4


class Workset(BaseModel):
    id: str = str(uuid4())
    ef_id: str | None = None
    name: str | None = None
    description: str | None = None
    volumes: list | None = None
    disabled_volumes: list | None = None

    def __repr__(self) -> str:
        return f"models.Workset(id={self.id[-11:]}, name={self.name}, ef_workset={self.ef_id!r})"
