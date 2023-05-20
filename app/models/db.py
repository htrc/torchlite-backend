from pydantic import BaseModel
from uuid import uuid4


class Dashboard(BaseModel):
    id: str = str(uuid4())
    name: str = "anonymous dashboard"
    workset: str | None = None

    def __repr__(self) -> str:
        return f"models.Dashboard(id={self.id[-11:]}, name={self.name})"


class Workset(BaseModel):
    id: str = str(uuid4())
    ef_id: str = ""
    name: str = "anonymous workset"

    def __repr__(self) -> str:
        return f"models.Workset(id={self.id[-11:]}, name={self.name}, ef_workset={self.ef_workset_id!r})"
