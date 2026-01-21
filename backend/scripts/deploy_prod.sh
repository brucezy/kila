#!/bin/bash
# scripts/deploy_prod.sh
# Deploy to production environment

echo "🚀 Deploying to PRODUCTION environment..."

# Strict error handling
set -e
set -u
set -o pipefail

# Validate environment file exists
if [ ! -f .env.production ]; then
    echo "❌ ERROR: .env.production not found!"
    exit 1
fi

# Set environment
export ENVIRONMENT=production

# Copy environment file
cp .env.production .env

# Install dependencies
pip install -r requirements.txt --no-cache-dir

# Run database migrations
python scripts/init_db.py

# Health check before starting
echo "Running pre-deployment checks..."
python -c "from app.config import settings; assert settings.is_production"

# Run with gunicorn
gunicorn app.main:app \
    --workers 8 \
    --worker-class uvicorn.workers.UvicornWorker \
    --bind 0.0.0.0:8000 \
    --timeout 120 \
    --graceful-timeout 30 \
    --access-logfile /var/log/app/access.log \
    --error-logfile /var/log/app/error.log \
    --log-level warning