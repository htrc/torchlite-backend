import httpx
import ssl
from .config import config

http_timeout = httpx.Timeout(5.0, read=None)
ctx = ssl.create_default_context()
ctx.load_cert_chain(certfile=config.REGISTRY_TLS_CERT_PATH, keyfile=config.REGISTRY_TLS_KEY_PATH)
print(ctx)
http = httpx.AsyncClient(follow_redirects=True, timeout=http_timeout, verify=ctx)