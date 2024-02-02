from contextlib import asynccontextmanager
from typing import List, TypeVar, Type, AsyncIterable

import httpx
from fastapi import status

from . import models
from .exceptions import EfApiError
from ..config import config
from ..http_client import http
from ..utils import sanitize

T = TypeVar('T')


class EfApi:
    def __init__(self, ef_api_url: str, http_client: httpx.AsyncClient):
        self.ef_api_url = ef_api_url
        self.http = http_client

    @asynccontextmanager
    @classmethod
    async def session(cls: Type[T], ef_api_url: str, *args, **kwargs) -> AsyncIterable[T]:
        async with httpx.AsyncClient(*args, **kwargs) as http_client:
            yield cls(ef_api_url=ef_api_url, http_client=http_client)

    async def _get(self, *args, **kwargs) -> dict:
        try:
            response = await self.http.get(*args, **kwargs)
            response.raise_for_status()
        except httpx.HTTPError as e:
            raise EfApiError(f"HTTP Exception for {e.request.url} - {e}")

        data = response.json()

        if data["code"] == status.HTTP_200_OK:
            return data.get("data")
        else:
            raise EfApiError(f"EF API Exception for {response.url} - {data}")

    async def get_workset(self, wsid: str, **kwargs) -> models.Workset:
        data = await self._get(f"{self.ef_api_url}/worksets/{wsid}", **kwargs)
        return models.Workset(**data)

    async def get_workset_metadata(self, wsid: str, fields: list[str] | None = None, **kwargs) -> List[models.Volume]:
        data = await self._get(
            f"{self.ef_api_url}/worksets/{wsid}/metadata",
            params={"fields": ",".join(fields or [])},
            **kwargs
        )
        return [models.Volume(**sanitize(vol)) for vol in data]

    async def get_workset_volumes(self,
                                  wsid: str,
                                  fields: list[str] | None = None,
                                  include_pos: bool = False,
                                  **kwargs) -> List[models.Volume]:
        data = await self._get(
            f"{self.ef_api_url}/worksets/{wsid}/volumes",
            params={
                "fields": ",".join(fields or []),
                "pos": include_pos,
            },
            **kwargs
        )
        return [models.Volume(**sanitize(vol)) for vol in data]


ef_api = EfApi(ef_api_url=config.EF_API_URL, http_client=http)
