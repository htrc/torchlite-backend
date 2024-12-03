import httpx
from .config import config

http_timeout = httpx.Timeout(5.0, read=None)
#cert = (config.REGISTRY_TLS_CERT,config.REGISTRY_TLS_KEY) if config.REGISTRY_TLS_CERT and config.REGISTRY_TLS_KEY else None
http = httpx.AsyncClient(follow_redirects=True, timeout=http_timeout)