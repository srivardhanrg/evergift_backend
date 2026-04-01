#!/bin/sh
# Docker entrypoint script for MagicTales backend
# Determines whether to run web server or worker based on SERVICE_TYPE env var

set -e

# Default to web service if SERVICE_TYPE is not set
SERVICE_TYPE=${SERVICE_TYPE:-web}

echo "=========================================="
echo "MagicTales Backend - Docker Entrypoint"
echo "=========================================="
echo "Service Type: $SERVICE_TYPE"
echo "Environment: ${APP_ENV:-development}"
echo "=========================================="

if [ "$SERVICE_TYPE" = "worker" ]; then
    echo "Starting ARQ Worker..."
    echo "Command: python -m arq app.worker.WorkerSettings"
    echo "=========================================="
    exec python -m arq app.worker.WorkerSettings
elif [ "$SERVICE_TYPE" = "web" ]; then
    echo "Starting Web Server (Gunicorn + Uvicorn)..."
    echo "Workers: 2"
    echo "Port: 8000"
    echo "=========================================="
    exec gunicorn app.main:app \
        -w 2 \
        -k uvicorn.workers.UvicornWorker \
        -b 0.0.0.0:8000 \
        --graceful-timeout 120 \
        --timeout 600 \
        --worker-tmp-dir /dev/shm
else
    echo "ERROR: Unknown SERVICE_TYPE: $SERVICE_TYPE"
    echo "Valid values: web, worker"
    exit 1
fi
