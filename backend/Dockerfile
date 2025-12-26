FROM python:3.11-slim

WORKDIR /app
RUN apt-get update && apt-get install -y gcc libpq-dev

# Install Poetry
RUN pip install poetry

COPY pyproject.toml poetry.lock ./

# Install dependencies
# We use "--no-root" to strictly install dependencies without the current project package yet
RUN poetry config virtualenvs.create false && poetry install --no-root

COPY . .
RUN chmod +x scripts/start.sh

EXPOSE 8000
CMD ["./scripts/start.sh"]