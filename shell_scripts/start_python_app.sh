#!/bin/sh

alembic upgrade head

cd ./src

python main.py
