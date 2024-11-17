#!/bin/sh

cd /app

alembic upgrade head

cd ./src

exec "$@"
