from pydantic import BaseModel
from uuid import uuid4


class Workset(BaseModel):
    id: str = str(uuid4())
    ef_workset_id: str = ""
    name: str = "anonymous workset"

    def __repr__(self) -> str:
        return f"torchlite.Workset(id={self.id[-11:]}, name={self.name}, ef_workset={self.ef_workset_id!r})"


class Dashboard(BaseModel):
    id: str = str(uuid4())
    name: str = "anonymous dashboard"
    workset: Workset | None = None

    def __repr__(self) -> str:
        return f"torchlite.Dashboard(id={self.id[-11:]}, name={self.name})"
