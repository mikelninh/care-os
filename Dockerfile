FROM python:3.12.13-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    CAREOS_DATA_MODE=synthetic

WORKDIR /opt/careos

RUN groupadd --system --gid 10001 careos \
    && useradd --system --uid 10001 --gid careos --create-home --home-dir /home/careos careos

COPY requirements.txt ./requirements.txt
COPY requirements.lock ./requirements.lock
RUN python -m pip install --upgrade pip \
    && python -m pip install --requirement requirements.lock

COPY --chown=careos:careos app ./app
COPY --chown=careos:careos architecture ./architecture
COPY --chown=careos:careos scripts ./scripts
COPY --chown=careos:careos deploy ./deploy
COPY --chown=careos:careos pilot_protocol.json ./pilot_protocol.json

USER 10001:10001

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
  CMD python -c "import json,urllib.request; r=urllib.request.urlopen('http://127.0.0.1:8000/api/health', timeout=3); d=json.load(r); raise SystemExit(0 if r.status==200 and d.get('status')=='ok' else 1)"

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--proxy-headers"]
