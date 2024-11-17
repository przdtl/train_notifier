#!/bin/sh

workers_count=${CELERY_WORKERS_COUNT:-1}

celery -A common.celery worker -l INFO --concurrency=$workers_count
