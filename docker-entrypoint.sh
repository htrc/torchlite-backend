#!/bin/sh

set -e

[ -f .venv/bin/activate ] && . .venv/bin/activate

if [ -r log_conf.yaml ]; then
  LOG_EXTRA="--log-config log_conf.yaml"
fi

eval exec uvicorn htrc.torchlite.app:api --host 0.0.0.0 --port "${TORCHLITE_PORT:-8000}" --proxy-headers "$LOG_EXTRA"
