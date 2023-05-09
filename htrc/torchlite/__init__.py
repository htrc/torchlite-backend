# -*- coding: utf-8 -*-
from enum import Enum
from typing import List, Optional
from pydantic import BaseModel

from importlib.metadata import version, PackageNotFoundError

try:
    __version__ = version("torchlite")
except PackageNotFoundError:
    __version__ = "UNKNOWN"


class Status(str, Enum):
    success = "success"
    error = "error"


class Response(BaseModel):
    status: Status
    data: Optional[List] = None
    messages: Optional[List[str]] = None
