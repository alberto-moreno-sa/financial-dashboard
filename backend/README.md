# 🐍 Backend - Financial Dashboard API

FastAPI-based REST API for portfolio management and financial data processing.

---

## 🏗️ Architecture

```
backend/src/
├── api/v1/          # API endpoints (auth, portfolio, upload)
├── core/            # Configuration (DB, Auth0, Settings)
├── models/          # SQLAlchemy ORM models
├── schemas/         # Pydantic DTOs
├── services/        # Business logic (PDF parser, snapshots)
└── main.py          # FastAPI app entry
```

**Full Documentation**: [../docs/ARCHITECTURE.md](../docs/ARCHITECTURE.md)

---

## 🚀 Quick Start

### Docker (Recommended)
```bash
docker-compose up -d
# Access: http://localhost:8000/docs
```

### Local Development
```bash
cd backend
poetry install && poetry shell
alembic upgrade head
uvicorn src.main:app --reload
```

**Setup Guide**: [../docs/BACKEND_SETUP.md](../docs/BACKEND_SETUP.md)

---

## 📚 Documentation

- [Backend Setup Guide](../docs/BACKEND_SETUP.md)
- [Architecture Overview](../docs/ARCHITECTURE.md)
- [Docker Guide](../docs/DOCKER_GUIDE.md)
- [API Docs](http://localhost:8000/docs) (when running)
