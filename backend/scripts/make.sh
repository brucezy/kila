# Makefile
# Convenient commands for different environments

.PHONY: dev beta prod install test

install:
	pip install -r requirements.txt

dev:
	export ENVIRONMENT=development && \
	cp .env.development .env && \
	uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

beta:
	export ENVIRONMENT=beta && \
	cp .env.beta .env && \
	uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4

prod:
	export ENVIRONMENT=production && \
	cp .env.production .env && \
	gunicorn app.main:app \
		--workers 8 \
		--worker-class uvicorn.workers.UvicornWorker \
		--bind 0.0.0.0:8000

test:
	export ENVIRONMENT=development && \
	pytest tests/ -v

init-db:
	python scripts/init_db.py

clean:
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete