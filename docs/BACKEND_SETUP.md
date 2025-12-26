# 🐍 Backend Setup Guide - Financial Dashboard API

**Stack**: FastAPI + Python 3.11 + PostgreSQL + SQLAlchemy

---

## 📋 Table of Contents

1. [Prerequisites](#prerequisites)
2. [Option 1: Docker Development](#option-1-docker-development-recommended)
3. [Option 2: Local Development](#option-2-local-development)
4. [Environment Variables Configuration](#environment-variables-configuration)
5. [Database Migrations](#database-migrations)
6. [Useful Commands](#useful-commands)
7. [Testing](#testing)
8. [Troubleshooting](#troubleshooting)

---

## 📦 Prerequisites

### For Docker Development
- **Docker Desktop** (includes Docker Compose)
- **Git**

### For Local Development
- **Python 3.11+**
- **Poetry** (dependency manager)
- **PostgreSQL 15+**
- **Git**

---

## 🐳 Option 1: Docker Development (Recommended)

This is the easiest and fastest way to get started.

### Step 1: Clone the Repository

```bash
git clone <repository-url>
cd financial-dashboard
```

### Step 2: Configure Environment Variables

```bash
# Copy the example file
cp .env.example .env

# Edit the .env file with your values
nano .env  # or use your favorite editor
```

**Minimum required configuration**:
```env
# Database
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_DB=financial_db

# Auth0 (obtain from https://manage.auth0.com)
AUTH0_DOMAIN=your-tenant.auth0.com
AUTH0_AUDIENCE=https://your-api-audience.com

# Security (generate with: openssl rand -hex 32)
SECRET_KEY=your_secret_key_here

# Frontend Auth0
VITE_AUTH0_DOMAIN=your-tenant.auth0.com
VITE_AUTH0_CLIENT_ID=your_client_id
VITE_AUTH0_AUDIENCE=https://your-api-audience.com
```

### Step 3: Start the Services

```bash
# Build and start all services
docker-compose up --build

# Or in detached mode (background)
docker-compose up -d
```

This will start:
- ✅ PostgreSQL on port **5432**
- ✅ Backend (FastAPI) on port **8000**
- ✅ Frontend (React) on port **5173**

### Step 4: Verify the Backend is Running

```bash
# View backend logs
docker-compose logs -f backend

# Should display:
# INFO: Uvicorn running on http://0.0.0.0:8000
```

Access:
- **API**: http://localhost:8000
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### Step 5: Development with Hot Reload

The code is mounted as a volume, so changes are reflected automatically:

```bash
# Edit any file in backend/src/
# The server will restart automatically
```

### Useful Docker Commands

```bash
# View container status
docker-compose ps

# View logs from all services
docker-compose logs -f

# View logs from backend only
docker-compose logs -f backend

# Restart the backend
docker-compose restart backend

# Stop all services
docker-compose down

# Stop and remove volumes (⚠️ deletes the database)
docker-compose down -v

# Access the backend container shell
docker-compose exec backend bash

# Execute Python commands inside the container
docker-compose exec backend python -c "print('Hello')"

# Run migrations
docker-compose exec backend alembic upgrade head

# Create new migration
docker-compose exec backend alembic revision --autogenerate -m "description"
```

---

## 💻 Option 2: Local Development

For local development without Docker.

### Step 1: Install Python and Poetry

```bash
# Check Python version
python --version  # Should be 3.11+

# Install Poetry (if you don't have it)
curl -sSL https://install.python-poetry.org | python3 -
```

### Step 2: Install PostgreSQL

**macOS (Homebrew)**:
```bash
brew install postgresql@15
brew services start postgresql@15
```

**Ubuntu/Debian**:
```bash
sudo apt update
sudo apt install postgresql postgresql-contrib
sudo systemctl start postgresql
```

**Windows**:
- Download from https://www.postgresql.org/download/windows/

### Step 3: Create Database

```bash
# Connect to PostgreSQL
psql postgres

# Create user and database
CREATE USER postgres WITH PASSWORD 'postgres';
CREATE DATABASE financial_db OWNER postgres;
GRANT ALL PRIVILEGES ON DATABASE financial_db TO postgres;

# Exit
\q
```

### Step 4: Configure Environment Variables

```bash
cd backend

# Copy example file
cp .env.example .env

# Edit with your values
nano .env
```

**Important**: Change `POSTGRES_SERVER` for local development:
```env
# For local development (NOT Docker)
POSTGRES_SERVER=localhost  # Instead of "db"

# Rest of configuration
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_DB=financial_db
POSTGRES_PORT=5432

# Auth0
AUTH0_DOMAIN=your-tenant.auth0.com
AUTH0_AUDIENCE=https://your-api-audience.com

# Security
SECRET_KEY=your_secret_key_here

# CORS
BACKEND_CORS_ORIGINS="http://localhost:5173,http://localhost:3000"
```

### Step 5: Install Dependencies

```bash
cd backend

# Install dependencies with Poetry
poetry install

# Activate the virtual environment
poetry shell
```

### Step 6: Run Migrations

```bash
# Inside Poetry virtual environment
alembic upgrade head
```

### Step 7: Start the Server

```bash
# Development mode (with hot reload)
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000

# Or using the script
chmod +x scripts/start.sh
./scripts/start.sh
```

The server will be available at:
- **API**: http://localhost:8000
- **Docs**: http://localhost:8000/docs

### Local Development - Useful Commands

```bash
# Activate virtual environment
cd backend
poetry shell

# Install new dependency
poetry add package-name

# Update dependencies
poetry update

# View installed dependencies
poetry show

# Run migrations
alembic upgrade head

# Create new migration
alembic revision --autogenerate -m "description"

# View migration history
alembic history

# Rollback last migration
alembic downgrade -1

# Run tests
pytest

# Run with coverage
pytest --cov=src tests/

# Linter
black src/
flake8 src/

# Type checking
mypy src/
```

---

## 🔧 Environment Variables Configuration

### Complete `.env` File

```env
# ========================================
# App Configuration
# ========================================
PROJECT_NAME="Financial Dashboard API"
API_V1_STR="/api/v1"
ENVIRONMENT="development"
DEBUG=True

# ========================================
# Auth0 Configuration
# ========================================
# Obtain from: https://manage.auth0.com
AUTH0_DOMAIN=your-tenant.auth0.com
AUTH0_AUDIENCE=https://your-api-audience.com

# ========================================
# Security (JWT - Legacy)
# ========================================
# Generate with: openssl rand -hex 32
SECRET_KEY="change_this_to_a_secure_random_string"
ACCESS_TOKEN_EXPIRE_MINUTES=60

# ========================================
# CORS: Allowed origins
# ========================================
BACKEND_CORS_ORIGINS="http://localhost:5173,http://localhost:3000,http://localhost:8000"

# ========================================
# Database Configuration
# ========================================
POSTGRES_SERVER=db               # "localhost" for local development
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_DB=financial_db
POSTGRES_PORT=5432

# ========================================
# Optional: Logging
# ========================================
LOG_LEVEL=INFO
```

### Generate Secure SECRET_KEY

```bash
# Option 1: OpenSSL
openssl rand -hex 32

# Option 2: Python
python -c "import secrets; print(secrets.token_hex(32))"
```

### Obtain Auth0 Credentials

1. Go to https://manage.auth0.com
2. Create a new application (Single Page Application)
3. Create a new API
4. Copy:
   - **Domain**: `your-tenant.auth0.com`
   - **Client ID**: for the frontend
   - **Audience**: Your API URL

---

## 🗄️ Database Migrations

### Basic Concepts

Migrations are managed with **Alembic**.

### Migration Structure

```
backend/migrations/
├── versions/           # Migration files
│   ├── d6c2d9c812eb_init.py
│   └── 6b57847ed974_add_users_table.py
├── env.py             # Alembic configuration
└── script.py.mako     # Template for migrations
```

### Main Commands

```bash
# Apply all pending migrations
alembic upgrade head

# Apply up to a specific migration
alembic upgrade <revision_id>

# Rollback last migration
alembic downgrade -1

# Rollback to a specific revision
alembic downgrade <revision_id>

# View current state
alembic current

# View history
alembic history

# View history with details
alembic history --verbose
```

### Create New Migration

**Automatic Migration** (recommended):
```bash
# Alembic detects changes in models and generates the migration
alembic revision --autogenerate -m "add new column"
```

**Manual Migration**:
```bash
# Creates an empty file to edit manually
alembic revision -m "description"
```

### Example of Manual Migration

```python
"""add user profile fields

Revision ID: abc123
Revises: xyz456
Create Date: 2025-01-15 10:30:00

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers
revision = 'abc123'
down_revision = 'xyz456'

def upgrade():
    op.add_column('users', sa.Column('bio', sa.String(500), nullable=True))
    op.add_column('users', sa.Column('phone', sa.String(20), nullable=True))

def downgrade():
    op.drop_column('users', 'phone')
    op.drop_column('users', 'bio')
```

### Migration Workflow

```bash
# 1. Modify models in src/models/
# Example: Add field to User model

# 2. Generate automatic migration
alembic revision --autogenerate -m "add bio field to users"

# 3. Review the generated file in migrations/versions/
# Verify that the changes are correct

# 4. Apply migration
alembic upgrade head

# 5. Verify in the database
psql financial_db -c "\d users"
```

### Reset Database

⚠️ **CAUTION**: This deletes all data

```bash
# Option 1: With Docker
docker-compose down -v
docker-compose up -d

# Option 2: Local
psql postgres -c "DROP DATABASE financial_db;"
psql postgres -c "CREATE DATABASE financial_db OWNER postgres;"
alembic upgrade head
```

---

## 🧪 Testing

### Test Structure

```
backend/tests/
├── __init__.py
├── conftest.py           # Pytest fixtures
├── test_auth.py          # Authentication tests
├── test_portfolio.py     # Portfolio tests
└── test_upload.py        # Upload tests
```

### Run Tests

```bash
# All tests
pytest

# Specific tests
pytest tests/test_auth.py

# With coverage
pytest --cov=src tests/

# With details
pytest -v

# Only marked tests
pytest -m "slow"
```

### Test Example

```python
import pytest
from httpx import AsyncClient
from src.main import app

@pytest.mark.asyncio
async def test_health_check():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/api/v1/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"
```

---

## 🔍 Useful Commands

### Verify Configuration

```bash
# View SQLAlchemy configuration
python -c "from src.core.config import settings; print(settings.SQLALCHEMY_DATABASE_URI)"

# Verify database connection
psql -h localhost -U postgres -d financial_db -c "SELECT version();"

# List tables
psql -h localhost -U postgres -d financial_db -c "\dt"

# Verify Auth0 config
python -c "from src.core.config import settings; print(f'Domain: {settings.AUTH0_DOMAIN}')"
```

### Debug

```bash
# Run with debug active
uvicorn src.main:app --reload --log-level debug

# View SQL queries
# Edit src/core/database.py:
engine = create_async_engine(
    settings.SQLALCHEMY_DATABASE_URI,
    echo=True  # ← Enable SQL logging
)
```

### Linting and Formatting

```bash
# Format code with Black
black src/

# Check style with flake8
flake8 src/

# Sort imports
isort src/

# Type checking with mypy
mypy src/
```

### Database Access

```bash
# With Docker
docker-compose exec db psql -U postgres -d financial_db

# Local
psql -h localhost -U postgres -d financial_db

# Useful psql commands
\dt          # List tables
\d users     # Describe users table
\l           # List databases
\q           # Exit
```

---

## 🐛 Troubleshooting

### Error: "Connection refused" when connecting to PostgreSQL

**With Docker**:
```bash
# Verify the container is running
docker-compose ps

# If not, start it
docker-compose up -d db
```

**Local**:
```bash
# Verify PostgreSQL is running
# macOS
brew services list

# Linux
sudo systemctl status postgresql

# Start if stopped
brew services start postgresql@15  # macOS
sudo systemctl start postgresql     # Linux
```

### Error: "ModuleNotFoundError: No module named 'src'"

```bash
# Make sure you're in the virtual environment
poetry shell

# Reinstall dependencies
poetry install
```

### Error: "Alembic can't locate revision"

```bash
# View state
alembic current

# Mark as current revision
alembic stamp head
```

### Error: "Auth0 domain not set"

```bash
# Verify that .env exists and has AUTH0_DOMAIN
cat backend/.env | grep AUTH0

# Restart the server after editing .env
```

### Error: "Table already exists" in migrations

```bash
# Option 1: Mark migration as applied
alembic stamp head

# Option 2: Reset database (⚠️ deletes data)
docker-compose down -v
docker-compose up -d
```

### Hot Reload Not Working

**With Docker**:
```bash
# Verify the volume is mounted
docker-compose config | grep volumes

# Restart container
docker-compose restart backend
```

**Local**:
```bash
# Make sure to use --reload
uvicorn src.main:app --reload
```

### Port 8000 Already in Use

```bash
# See which process is using the port
lsof -i :8000

# Kill the process
kill -9 <PID>

# Or use another port
uvicorn src.main:app --reload --port 8001
```

---

## 📚 Additional Resources

### Official Documentation
- [FastAPI](https://fastapi.tiangolo.com)
- [SQLAlchemy](https://docs.sqlalchemy.org/en/20/)
- [Alembic](https://alembic.sqlalchemy.org/en/latest/)
- [Poetry](https://python-poetry.org/docs/)
- [Pydantic](https://docs.pydantic.dev/)

### Tutorials
- [FastAPI Best Practices](https://github.com/zhanymkanov/fastapi-best-practices)
- [SQLAlchemy Async Tutorial](https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html)

---

## ✅ Setup Completion Checklist

- [ ] Docker installed and running
- [ ] Repository cloned
- [ ] `.env` file configured
- [ ] Services started with `docker-compose up`
- [ ] Backend accessible at http://localhost:8000
- [ ] Swagger UI accessible at http://localhost:8000/docs
- [ ] Migrations applied
- [ ] Auth0 configured

---

**Ready to develop! 🚀**
