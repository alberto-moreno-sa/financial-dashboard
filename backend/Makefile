# Makefile en backend/

# Detectar si estamos en Docker o Local para ajustar la URL de la DB
# Si estamos en local, forzamos localhost.
DB_URL_LOCAL=postgresql+asyncpg://postgres:postgres@localhost:5432/financial_db

.PHONY: install migrate upgrade run

# Instalar todo lo necesario
install:
	poetry install

# Crear una nueva migración (Uso: make migrate m="Nombre de la migracion")
migrate:
	DATABASE_URL=$(DB_URL_LOCAL) poetry run alembic revision --autogenerate -m "$(m)"

# Aplicar cambios a la DB
upgrade:
	DATABASE_URL=$(DB_URL_LOCAL) poetry run alembic upgrade head

# Correr el servidor localmente
run:
	DATABASE_URL=$(DB_URL_LOCAL) poetry run uvicorn src.main:app --reload