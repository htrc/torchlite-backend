import httpx
import ssl
from .config import config

http_timeout = httpx.Timeout(5.0, read=None)
http = httpx.AsyncClient(follow_redirects=True, timeout=http_timeout)

try:
  ctx = ssl.create_default_context()
  ctx.load_cert_chain(certfile=config.REGISTRY_TLS_CERT_PATH, keyfile=config.REGISTRY_TLS_KEY_PATH)
  registry_http = httpx.AsyncClient(follow_redirects=True, timeout=http_timeout, verify=ctx)
except TypeError:
  registry_http = http