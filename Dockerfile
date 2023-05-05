FROM python:3.11-slim

ENV TORCHLITE_PORT 8000

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED 1
ENV PYTHONFAULTHANDLER 1
ENV PYTHONHASHSEED random
ENV PIP_NO_CACHE_DIR 1

ENV TINI_VERSION v0.19.0
ADD https://github.com/krallin/tini/releases/download/${TINI_VERSION}/tini /tini
ADD https://github.com/krallin/tini/releases/download/${TINI_VERSION}/tini.asc /tini.asc
RUN chmod +x /tini

RUN useradd -ms /bin/bash torchlite
WORKDIR /home/torchlite

COPY dist/*.whl log_conf.yaml docker-entrypoint.sh ./

RUN pip install -U pip *.whl && rm -f *.whl

USER torchlite

EXPOSE $TORCHLITE_PORT

ENTRYPOINT ["/tini", "--"]
CMD ["./docker-entrypoint.sh"]
