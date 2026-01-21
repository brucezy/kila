#!/bin/bash
# scripts/deploy_dev.sh
# Deploy to development environment

echo "🚀 Deploying to DEVELOPMENT environment..."

# Set environment
export ENVIRONMENT=development

# Copy environment file
cp .env.development .env

# Install dependencies
pip install -r requirements.txt

# Initialize database
python scripts/init_db.py

# Run development server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
