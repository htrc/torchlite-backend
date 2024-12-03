import httpx
from .config import config

http_timeout = httpx.Timeout(5.0, read=None)
print("Have cert")
print("True" if config.REGISTRY_TLS_CERT else "False")
print("Have key")
print("True" if config.REGISTRY_TLS_KEY else "False")
#cert = (config.REGISTRY_TLS_CERT,config.REGISTRY_TLS_KEY) if config.REGISTRY_TLS_CERT and config.REGISTRY_TLS_KEY else None
http = httpx.AsyncClient(follow_redirects=True, timeout=http_timeout, cert=None)