FROM debian:stretch

EXPOSE 8000
WORKDIR /srv/portra

RUN apt-get update \
    && DEBIAN_FRONTEND=noninteractive apt-get upgrade -y \
    && DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        make \
        python3 \
        python3-dev \
        virtualenv \
        libexempi3 \
    && apt-get clean

COPY . /srv/portra

RUN openssl rand -base64 32 >> /srv/portra/SECRET_KEY
RUN mkdir /srv/portra/files /srv/portra/files/i /srv/portra/files/m

RUN virtualenv -p python3 /srv/portra/venv \
    && /srv/portra/venv/bin/pip install gunicorn \
    && /srv/portra/venv/bin/pip install -r /srv/portra/requirements.txt

ENV PYTHONUNBUFFERED TRUE
ENV PORTRA_SETTINGS /srv/portra/settings/fs_prod.py

CMD [ \
    "/srv/portra/venv/bin/gunicorn", \
        "--bind", "0.0.0.0:8000", \
        "--workers", "4", \
        "portra.app:app" \
]

