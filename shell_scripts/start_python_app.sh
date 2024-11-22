#!/bin/sh

cd ..

alembic upgrade head

cd ./src

python main.py
