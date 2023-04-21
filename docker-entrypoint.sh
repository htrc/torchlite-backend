#!/bin/sh

set -e

. .venv/bin/activate

exec uvicorn htrc.torchlite.app:api --host 0.0.0.0 --port $TORCHLITE_PORT --proxy-headers
