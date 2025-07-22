# Makefile for FastAPI + Alembic + PostgreSQL (Docker)

# Load environment variables from .env
include .env
export $(shell sed 's/=.*//' .env)

# Docker
up:
	docker compose up -d

down:
	docker compose down

restart:
	docker compose down && docker compose up -d

logs:
	docker compose logs -f web

ps:
	docker compose ps

# Alembic (migrations)
migrate:
	docker compose run --rm web alembic upgrade head

revision:
	docker compose run --rm web alembic revision --autogenerate -m "$(m)"

downgrade:
	docker compose run --rm web alembic downgrade -1

current:
	docker compose run --rm web alembic current

# App shell
shell:
	docker compose run --rm web bash

# FastAPI
serve:
	docker compose run --rm web uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
