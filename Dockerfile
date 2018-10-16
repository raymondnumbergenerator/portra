FROM debian:stretch

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
RUN mkdir /srv/portra/i /srv/portra/m

RUN virtualenv -p python3 /srv/portra/venv \
    && /srv/portra/venv/bin/pip install gunicorn \
    && /srv/portra/venv/bin/pip install -r /srv/portra/requirements.txt

EXPOSE 8000
ENV PYTHONUNBUFFERED TRUE
ENV PORTRA_SETTINGS /srv/portra/settings/fs_prod.py

WORKDIR /srv/portra
CMD [ \
    "/srv/portra/venv/bin/gunicorn", \
        "--bind", "0.0.0.0:8000", \
        "--workers", "4", \
        "portra.app:app" \
]

