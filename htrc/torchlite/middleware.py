from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import Response
from timeit import default_timer as timer
from htrc.torchlite import __version__


class TorchliteVersionHeaderMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        response = await call_next(request)
        response.headers["X-Torchlite-Version"] = __version__
        return response


class TimingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        start = timer()
        response = await call_next(request)
        elapsed = timer() - start
        response.headers["X-Torchlite-ResponseTime"] = f'{elapsed * 1000:.0f}'
        return response
