# Financial Dashboard System

A comprehensive personal financial management system for tracking investment portfolios with automated PDF parsing and bulk upload capabilities.

---

## 📋 Table of Contents

1. [Problem Statement](#-problem-statement)
2. [Solution](#-solution)
3. [Tech Stack](#-tech-stack)
4. [Quick Start](#-quick-start)
5. [Project Structure](#-project-structure)
6. [Key Features](#-key-features)
7. [Documentation](#-documentation)
8. [Development Guide](#-development-guide)
9. [Contributing](#-contributing)
10. [License](#️-license--copyright)

---

## 🎯 Problem Statement

### The Challenge

Managing investment portfolios across multiple brokerage accounts is time-consuming and error-prone when done manually. Investors typically face several pain points:

1. **Manual Data Entry**: Copying data from PDF statements into spreadsheets is tedious and error-prone
2. **Historical Tracking**: Difficult to track portfolio evolution over time without a centralized system
3. **Duplicate Management**: Risk of importing the same statement multiple times
4. **Performance Analysis**: Calculating unrealized gains, cost basis, and portfolio allocation requires complex formulas
5. **Bulk Processing**: Processing multiple monthly statements (e.g., 2+ years of data) is extremely time-consuming

### Target User

Individual investors with brokerage accounts at **GBM (Grupo Bursátil Mexicano)** who want to:
- Automatically import their monthly statements
- Track portfolio performance over time
- Visualize asset allocation and gains/losses
- Process historical data in bulk (up to 100 statements at once)

---

## ✅ Solution

### What We Built

A full-stack web application that:

1. **Automates PDF Parsing**
   - Extracts portfolio data from GBM PDF statements using intelligent text parsing
   - Captures equity values, fixed income, cash positions, and individual holdings
   - Calculates unrealized gains and cost basis automatically

2. **Enables Bulk Upload**
   - Process up to 100 PDF files simultaneously
   - Intelligent duplicate detection using SHA-256 hashing + statement date
   - Independent error handling per file (one failure doesn't stop others)
   - Detailed status report for each file (success/duplicate/error)

3. **Provides Historical Tracking**
   - Stores monthly snapshots of portfolio composition
   - Tracks individual positions with cost basis and current values
   - Maintains upload history with audit trail

4. **Offers Real-Time Visualization**
   - Interactive dashboard with portfolio statistics
   - Holdings table with sortable columns
   - Snapshot history with evolution charts
   - Responsive UI with live data updates

### Technical Achievements

- **Async Architecture**: Fully async backend with SQLAlchemy 2.0 (async ORM)
- **Auth0 Integration**: Secure authentication with JWT validation
- **Multi-Tenant**: Data isolation per user
- **Hot Reload Development**: Docker volumes for instant code changes
- **Type Safety**: Pydantic V2 validation + TypeScript
- **Modern UI**: React 19 with Tailwind CSS v4

---

## 🚀 Tech Stack

### Backend ([/backend](backend/))
```
Python 3.11 + FastAPI
├── SQLAlchemy 2.0 (async ORM)
├── PostgreSQL 15 (AsyncPG driver)
├── Alembic (migrations)
├── Pydantic V2 (validation)
├── pdfplumber (PDF parsing)
├── Auth0 (JWT authentication)
└── Poetry (package management)
```

**README**: [backend/README.md](backend/README.md)

### Frontend ([/frontend](frontend/))
```
React 19 + TypeScript + Vite
├── React Router 7 (routing)
├── TanStack Query (server state)
├── Zustand (client state)
├── Tailwind CSS v4 (styling)
├── Radix UI (components)
├── Recharts (charts)
└── Auth0 React SDK (auth)
```

**README**: [frontend/README.md](frontend/README.md)

### Infrastructure
```
Docker + Docker Compose
├── PostgreSQL 15 (database)
├── Backend container (FastAPI)
└── Frontend container (Vite dev server)
```

---

## 🚀 Quick Start

### Option 1: Docker (Recommended)

```bash
# 1. Clone repository
git clone <repository-url>
cd financial-dashboard

# 2. Configure environment variables
cp .env.example .env
nano .env  # Add your Auth0 credentials

# 3. Start all services
docker-compose up -d

# 4. Access application
# - Frontend: http://localhost:5173
# - Backend API: http://localhost:8000/docs
```

**Detailed Guide**: [docs/DOCKER_GUIDE.md](docs/DOCKER_GUIDE.md)

### Option 2: Local Development

**Backend**:
```bash
cd backend
poetry install
poetry shell
alembic upgrade head
uvicorn src.main:app --reload
```

**Frontend**:
```bash
cd frontend
npm install
npm run dev
```

**Setup Guides**:
- [Backend Setup](docs/BACKEND_SETUP.md)
- [Frontend Setup](docs/FRONTEND_SETUP.md)

---

## 📁 Project Structure

```
financial-dashboard/
├── backend/                 # FastAPI backend
│   ├── src/
│   │   ├── api/v1/         # API endpoints
│   │   ├── core/           # Configuration
│   │   ├── models/         # SQLAlchemy models
│   │   ├── schemas/        # Pydantic DTOs
│   │   ├── services/       # Business logic
│   │   └── main.py         # App entry
│   ├── migrations/         # Alembic migrations
│   └── README.md          # Backend docs
│
├── frontend/               # React frontend
│   ├── app/
│   │   ├── routes/        # Pages
│   │   ├── features/      # Feature modules
│   │   ├── widgets/       # UI widgets
│   │   ├── entities/      # Domain models
│   │   └── shared/        # Shared utilities
│   └── README.md         # Frontend docs
│
├── docs/                   # Documentation
│   ├── ARCHITECTURE.md    # System architecture
│   ├── BACKEND_SETUP.md   # Backend setup guide
│   ├── FRONTEND_SETUP.md  # Frontend setup guide
│   └── DOCKER_GUIDE.md    # Docker guide
│
├── docker-compose.yml      # Container orchestration
├── .env.example           # Environment template
└── README.md              # This file
```

---

## 🌟 Key Features

### 1. Single PDF Upload
- Upload individual GBM PDF statements
- Automatic data extraction (portfolio summary + positions)
- Duplicate detection (hash + date)
- Real-time dashboard updates

### 2. Bulk Upload (Up to 100 Files)
- Drag & drop multiple PDFs
- Process all files independently
- Detailed results per file:
  - ✅ Success: File processed and saved
  - ⚠️ Duplicate: File already exists
  - ❌ Error: Processing failed (with details)
- Summary statistics (total, successful, duplicates, errors)

### 3. Portfolio Dashboard
- Total portfolio value
- Asset allocation (equity, fixed income, cash)
- Unrealized gains/losses
- Holdings table with:
  - Ticker symbols
  - Quantity
  - Cost basis
  - Current value
  - Gain/loss ($)
  - Gain/loss (%)

### 4. Snapshot History
- Monthly portfolio snapshots
- Evolution charts
- Historical comparison
- Period selection

### 5. Authentication & Security
- Auth0 integration (Google, GitHub, Email/Password)
- JWT token validation
- Multi-tenant data isolation
- Secure API endpoints

---

## 📚 Documentation

### 📖 Complete Guides

#### Setup & Installation
- **[Docker Guide](docs/DOCKER_GUIDE.md)** - Complete Docker setup (recommended)
  - Quick start with Docker Compose
  - Container architecture
  - Service configuration (DB, Backend, Frontend)
  - Volume management & persistence
  - Common commands
  - Backup & restore
  - Production setup
  - Troubleshooting

- **[Backend Setup](docs/BACKEND_SETUP.md)** - Backend installation guide
  - Docker setup
  - Local development setup
  - Environment variables configuration
  - Database migrations with Alembic
  - Common commands
  - Testing
  - Troubleshooting

- **[Frontend Setup](docs/FRONTEND_SETUP.md)** - Frontend installation guide
  - Docker setup
  - Local development setup
  - Environment variables configuration
  - Project structure (Feature-Sliced Design)
  - Auth0 configuration
  - Common commands
  - UI customization
  - Troubleshooting

#### Architecture & Design
- **[System Architecture](docs/ARCHITECTURE.md)** - Complete system overview
  - Tech stack details
  - High-level architecture
  - Project structure
  - Core components
  - Data flow diagrams
  - Database schema
  - API endpoints
  - Design patterns

#### Component Documentation
- **[Backend README](backend/README.md)** - Backend architecture & quick start
- **[Frontend README](frontend/README.md)** - Frontend architecture & quick start

### 📋 Documentation by Topic

#### Initial Setup
- [Docker Setup](docs/DOCKER_GUIDE.md#quick-start)
- [Backend Local Setup](docs/BACKEND_SETUP.md#option-2-local-development)
- [Frontend Local Setup](docs/FRONTEND_SETUP.md#option-2-local-development)
- [Environment Variables](docs/DOCKER_GUIDE.md#environment-variables)

#### Authentication
- [Auth0 Configuration](docs/FRONTEND_SETUP.md#auth0-configuration)
- [JWT Validation (Backend)](docs/ARCHITECTURE.md#authentication-and-authorization)
- [Auth0 React SDK](docs/FRONTEND_SETUP.md#auth0-configuration)

#### Database
- [Database Schema](docs/ARCHITECTURE.md#database)
- [Migrations with Alembic](docs/BACKEND_SETUP.md#database-migrations)
- [Backup & Restore](docs/DOCKER_GUIDE.md#backup-and-restore)

#### Development
- [Docker Commands](docs/DOCKER_GUIDE.md#common-commands)
- [Backend Commands](docs/BACKEND_SETUP.md#common-commands)
- [Frontend Commands](docs/FRONTEND_SETUP.md#common-commands)
- [Hot Reload](docs/DOCKER_GUIDE.md#development-with-hot-reload)

#### API
- [Available Endpoints](docs/ARCHITECTURE.md#api-endpoints)
- [Swagger Documentation](http://localhost:8000/docs)
- [Pydantic Schemas](docs/ARCHITECTURE.md#core-components)

#### Architecture
- [Tech Stack](docs/ARCHITECTURE.md#tech-stack)
- [Data Flow](docs/ARCHITECTURE.md#data-flow)
- [Design Patterns](docs/ARCHITECTURE.md#design-patterns)
- [Feature-Sliced Design](docs/FRONTEND_SETUP.md#project-structure)

#### Troubleshooting
- [Docker Troubleshooting](docs/DOCKER_GUIDE.md#troubleshooting)
- [Backend Troubleshooting](docs/BACKEND_SETUP.md#troubleshooting)
- [Frontend Troubleshooting](docs/FRONTEND_SETUP.md#troubleshooting)

### 🎯 Guide by Role

#### For New Developers
1. Read [System Architecture](docs/ARCHITECTURE.md) to understand the system
2. Follow [Docker Guide](docs/DOCKER_GUIDE.md) for initial setup
3. Review [Backend Setup](docs/BACKEND_SETUP.md) or [Frontend Setup](docs/FRONTEND_SETUP.md) based on your area

#### For Backend Developers
1. [Backend Setup](docs/BACKEND_SETUP.md) - Complete setup
2. [Architecture - Database](docs/ARCHITECTURE.md#database)
3. [Architecture - API Endpoints](docs/ARCHITECTURE.md#api-endpoints)

#### For Frontend Developers
1. [Frontend Setup](docs/FRONTEND_SETUP.md) - Complete setup
2. [Frontend - Project Structure](docs/FRONTEND_SETUP.md#project-structure)
3. [Architecture - Data Flow](docs/ARCHITECTURE.md#data-flow)

#### For DevOps
1. [Docker Guide](docs/DOCKER_GUIDE.md) - Complete orchestration
2. [Docker - Production](docs/DOCKER_GUIDE.md#production)
3. [Architecture - Deployment](docs/ARCHITECTURE.md#deployment)

### 🔗 External Documentation
- [FastAPI Docs](https://fastapi.tiangolo.com)
- [React Docs](https://react.dev)
- [React Router](https://reactrouter.com)
- [Docker Docs](https://docs.docker.com)
- [Auth0 Docs](https://auth0.com/docs)
- [SQLAlchemy](https://docs.sqlalchemy.org)
- [TanStack Query](https://tanstack.com/query)

### 🌐 Application URLs (Local)
- **Frontend**: http://localhost:5173
- **Backend API**: http://localhost:8000
- **API Docs (Swagger)**: http://localhost:8000/docs
- **API Docs (ReDoc)**: http://localhost:8000/redoc

---

## 💻 Development Guide

### Common Tasks

#### Start Development Environment
```bash
# Start everything
docker-compose up -d

# View logs
docker-compose logs -f

# Restart a service
docker-compose restart backend

# Stop everything
docker-compose down

# Clean restart (⚠️ deletes data)
docker-compose down -v && docker-compose up -d
```

#### Database Operations
```bash
# Run migrations
docker-compose exec backend alembic upgrade head

# Create migration
docker-compose exec backend alembic revision --autogenerate -m "description"

# Access PostgreSQL
docker-compose exec db psql -U postgres -d financial_db

# View tables
docker-compose exec db psql -U postgres -d financial_db -c "\dt"
```

#### Testing
```bash
# Backend tests
cd backend && poetry run pytest

# Frontend tests
cd frontend && npm test

# With coverage
cd backend && poetry run pytest --cov=src tests/
```

**More commands**: [docs/DOCKER_GUIDE.md#common-commands](docs/DOCKER_GUIDE.md#common-commands)

### Troubleshooting

**Port already in use**:
```bash
lsof -i :8000  # Find process
kill -9 <PID>   # Kill process
```

**Database connection refused**:
```bash
docker-compose ps db          # Check status
docker-compose restart db     # Restart
```

**Auth0 not working**:
1. Check [Auth0 Configuration Guide](docs/FRONTEND_SETUP.md#auth0-configuration)
2. Verify callback URLs in Auth0 dashboard
3. Ensure `.env` has correct credentials

**More solutions**: [docs/DOCKER_GUIDE.md#troubleshooting](docs/DOCKER_GUIDE.md#troubleshooting)

---

## 🤝 Contributing

### Git Workflow

1. Create branch from `develop`
2. Make changes
3. Write tests (if applicable)
4. Update documentation (if applicable)
5. Commit with descriptive message
6. Push and create Pull Request
7. Wait for code review

### Commit Convention
```
feat:     New feature
fix:      Bug fix
docs:     Documentation changes
style:    Code formatting
refactor: Code refactoring
test:     Tests
chore:    Build/tooling changes
```

### Branch Convention
```
main           # Production
develop        # Development
feature/name   # New feature
fix/name       # Bug fix
docs/name      # Documentation
```

### Onboarding Checklist

For new developers:

- [ ] Read [System Architecture](docs/ARCHITECTURE.md)
- [ ] Install Docker Desktop
- [ ] Clone repository
- [ ] Configure `.env` with credentials
- [ ] Run `docker-compose up`
- [ ] Verify access to frontend (5173) and backend (8000)
- [ ] Create Auth0 account (if needed)
- [ ] Make test change and verify hot reload
- [ ] Read specific guide ([Backend](docs/BACKEND_SETUP.md) or [Frontend](docs/FRONTEND_SETUP.md))
- [ ] Familiarize with code structure

---

## 📧 Contact

For questions or support, please contact the repository owner.

---

**Built with ❤️ using FastAPI, React, and Docker**

**Last Updated**: 2025-12-29
