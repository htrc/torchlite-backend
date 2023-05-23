from enum import Enum
from typing import Optional
from importlib.metadata import version, PackageNotFoundError
from pydantic import BaseModel


try:
    __version__ = version("torchlite")
except PackageNotFoundError:
    __version__ = "UNKNOWN"


class Status(str, Enum):
    success = "success"
    error = "error"


class Response(BaseModel):
    status: Status
    data: Optional[list] = None
    messages: Optional[list[str]] = None
