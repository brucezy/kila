#!/bin/bash
# scripts/deploy_beta.sh
# Deploy to beta/staging environment

echo "🚀 Deploying to BETA environment..."

# Set environment
export ENVIRONMENT=beta

# Copy environment file
cp .env.beta .env

# Install dependencies (use production-like setup)
pip install -r requirements.txt --no-cache-dir

# Run database migrations
python scripts/init_db.py

# Run with gunicorn (production-like)
gunicorn app.main:app \
    --workers 4 \
    --worker-class uvicorn.workers.UvicornWorker \
    --bind 0.0.0.0:8000 \
    --access-logfile - \
    --error-logfile -