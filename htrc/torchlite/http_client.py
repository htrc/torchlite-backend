import httpx
import ssl
from .config import config

http_timeout = httpx.Timeout(5.0, read=None)
ctx = ssl.create_default_context()
ctx.load_cert_chain(certfile=config.REGISTRY_TLS_CERT, keyfile=config.REGISTRY_TLS_KEY)
http = httpx.AsyncClient(follow_redirects=True, timeout=http_timeout, verify=ctx)