FROM python:3.12-alpine AS builder

WORKDIR /app

ENV PYTHONPATH=/app/src

COPY ./requirements.txt .

RUN pip install -r requirements.txt

COPY ./src ./src

COPY ./entrypoint.sh ./

RUN chmod +x ./entrypoint.sh

ENTRYPOINT ["sh", "./entrypoint.sh"]