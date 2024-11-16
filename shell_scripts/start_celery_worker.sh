#!/bin/sh

workers_count=${CELERY_WORKERS_COUNT:-1}

celery -A utils.celery worker -l INFO --concurrency=$workers_count
