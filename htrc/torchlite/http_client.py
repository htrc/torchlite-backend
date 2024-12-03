import httpx

http_timeout = httpx.Timeout(5.0, read=None)
http = httpx.AsyncClient(follow_redirects=True, timeout=http_timeout)