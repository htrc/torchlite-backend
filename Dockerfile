FROM python:3.11-slim as base

ARG ENV
ARG TORCHLITE_VERSION

# One of "prod" or "dev"
ENV ENV ${ENV}
ENV TORCHLITE_PORT 8000
ENV TORCHLITE_VERSION ${TORCHLITE_VERSION:-0.0.0}

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE 1
# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED 1
ENV PYTHONFAULTHANDLER 1
ENV PYTHONHASHSEED random

RUN useradd -ms /bin/bash torchlite
WORKDIR /home/torchlite

FROM base as builder

ENV PIP_DEFAULT_TIMEOUT 100
ENV PIP_DISABLE_PIP_VERSION_CHECK 1
ENV PIP_NO_CACHE_DIR 1
ENV POETRY_VERSION 1.4.2
ENV PATH "${PATH}:/root/.local/bin"

RUN pip install --upgrade pip pipx && pipx install "poetry==$POETRY_VERSION"

COPY poetry.lock pyproject.toml README.org ./
COPY htrc ./htrc

RUN poetry config virtualenvs.in-project true && \
    poetry install --no-interaction --no-ansi --no-root --only=main --sync && \
    poetry version $TORCHLITE_VERSION \
    poetry build --format=wheel

FROM base as final

COPY --chown=torchlite:torchlite --from=builder /home/torchlite/.venv ./.venv
COPY --chown=torchlite:torchlite --from=builder /home/torchlite/dist .
COPY --chown=torchlite:torchlite docker-entrypoint.sh .

USER torchlite

RUN ./.venv/bin/pip install *.whl

EXPOSE $TORCHLITE_PORT

CMD ["./docker-entrypoint.sh"]
