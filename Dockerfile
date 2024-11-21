FROM python:3.12-slim-bookworm AS builder

RUN apt-get update && apt-get install -y \
    build-essential curl \
    && rm -rf /var/lib/apt/lists/*

ENV POETRY_VERSION=1.8.4
RUN curl -sSL https://install.python-poetry.org | python3 -

ENV PATH="/root/.local/bin:$PATH" \
    POETRY_VIRTUALENVS_CREATE=false \
    POETRY_NO_INTERACTION=1

WORKDIR /app

COPY pyproject.toml poetry.lock ./
RUN poetry install --only main
RUN playwright install chromium

FROM python:3.12-slim-bookworm

COPY --from=builder /root/.cache/ms-playwright /root/.cache/ms-playwright
COPY --from=builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

RUN playwright install-deps chromium

WORKDIR /app

COPY src/ ./src/
COPY shell_scripts/ ./shell_scripts/
COPY alembic.ini .

ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app/src

ENTRYPOINT ["sh", "./shell_scripts/entrypoint.sh"]
