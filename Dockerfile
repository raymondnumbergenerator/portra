FROM debian:stretch
RUN apt-get update \
    && DEBIAN_FRONTEND=noninteractive apt-get upgrade -y \
    && DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-dev \
        virtualenv \
    && apt-get clean

RUN apt-get install libexempi3

EXPOSE 8000
ENV PYTHONBUFFERED TRUE

RUN make venv
RUN make secret
RUN make settings.py
CMD make dev

