# 🐳 Docker Complete Guide - Financial Dashboard

**Complete Stack**: PostgreSQL + FastAPI + React in Docker

---

## 📋 Table of Contents

1. [Overview](#overview)
2. [Prerequisites](#prerequisites)
3. [Quick Start](#quick-start)
4. [Docker Architecture](#docker-architecture)
5. [Services](#services)
6. [Environment Variables](#environment-variables)
7. [Volumes and Persistence](#volumes-and-persistence)
8. [Networking](#networking)
9. [Useful Commands](#useful-commands)
10. [Troubleshooting](#troubleshooting)
11. [Production](#production)

---

## 🎯 Overview

The project uses **Docker Compose** to orchestrate 3 services:

```
┌─────────────────────────────────────────────────┐
│              Docker Compose                     │
│                                                 │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐     │
│  │    DB    │  │ Backend  │  │ Frontend │     │
│  │          │  │          │  │          │     │
│  │PostgreSQL│←─│ FastAPI  │←─│  React   │     │
│  │  :5432   │  │  :8000   │  │  :5173   │     │
│  └──────────┘  └──────────┘  └──────────┘     │
└─────────────────────────────────────────────────┘
```

**Benefits**:
- ✅ Unified configuration for the entire team
- ✅ No need to install Python, Node.js, PostgreSQL locally
- ✅ Hot reload in development
- ✅ Easy environment reset
- ✅ Isolation between projects

---

## 📦 Prerequisites

### Install Docker Desktop

**macOS**:
```bash
# Option 1: Homebrew
brew install --cask docker

# Option 2: Download from
# https://www.docker.com/products/docker-desktop
```

**Windows**:
- Download from https://www.docker.com/products/docker-desktop
- Requires WSL 2

**Linux (Ubuntu)**:
```bash
# Install Docker Engine
sudo apt-get update
sudo apt-get install docker-ce docker-ce-cli containerd.io

# Install Docker Compose
sudo apt-get install docker-compose-plugin

# Add user to docker group
sudo usermod -aG docker $USER
newgrp docker
```

### Verify Installation

```bash
# Verify Docker
docker --version
# Docker version 24.0.0+

# Verify Docker Compose
docker-compose --version
# Docker Compose version v2.20.0+

# Verify Docker is running
docker ps
# Should not show errors
```

---

## 🚀 Quick Start

### 1. Clone and Configure

```bash
# Clone repository
git clone <repository-url>
cd financial-dashboard

# Copy environment variables
cp .env.example .env

# Edit .env with your credentials
nano .env
```

### 2. Configure Environment Variables

Edit `.env` in the project root:

```env
# Database
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_DB=financial_db

# Auth0 (obtain from https://manage.auth0.com)
AUTH0_DOMAIN=your-tenant.auth0.com
AUTH0_AUDIENCE=https://your-api-audience.com

# Backend Security
SECRET_KEY=your_secret_key_here

# Frontend Auth0
VITE_AUTH0_DOMAIN=your-tenant.auth0.com
VITE_AUTH0_CLIENT_ID=your_client_id
VITE_AUTH0_AUDIENCE=https://your-api-audience.com
```

### 3. Start Everything

```bash
# Build and start all services
docker-compose up --build

# Or in detached mode (background)
docker-compose up -d
```

### 4. Verify Everything Works

Wait a few seconds and verify:

```bash
# View service status
docker-compose ps

# Should display:
# NAME                   STATUS    PORTS
# financial_db           Up        0.0.0.0:5432->5432/tcp
# financial_backend      Up        0.0.0.0:8000->8000/tcp
# financial_frontend     Up        0.0.0.0:5173->5173/tcp
```

### 5. Access the Applications

- **Frontend**: http://localhost:5173
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

---

## 🏗️ Docker Architecture

### File Structure

```
financial-dashboard/
├── docker-compose.yml       # Services orchestration
├── .env                     # Environment variables
├── backend/
│   ├── Dockerfile           # Backend image
│   ├── .dockerignore        # Files to ignore
│   └── scripts/
│       └── start.sh         # Startup script
└── frontend/
    ├── Dockerfile           # Frontend image
    └── .dockerignore        # Files to ignore
```

### docker-compose.yml Overview

```yaml
services:
  # PostgreSQL Database
  db:
    image: postgres:15-alpine
    volumes:
      - postgres_data:/var/lib/postgresql/data
    environment:
      - POSTGRES_USER=${POSTGRES_USER:-postgres}
      - POSTGRES_PASSWORD=${POSTGRES_PASSWORD:-postgres}
      - POSTGRES_DB=${POSTGRES_DB:-financial_db}
    ports:
      - "5432:5432"

  # FastAPI Backend
  backend:
    build: ./backend
    volumes:
      - ./backend:/app  # Hot reload
    environment:
      - POSTGRES_SERVER=db
      - AUTH0_DOMAIN=${AUTH0_DOMAIN}
      - SECRET_KEY=${SECRET_KEY}
    depends_on:
      - db
    ports:
      - "8000:8000"

  # React Frontend
  frontend:
    build: ./frontend
    volumes:
      - ./frontend:/app  # Hot reload
    environment:
      - VITE_API_URL=${VITE_API_URL:-http://localhost:8000/api/v1}
      - VITE_AUTH0_DOMAIN=${VITE_AUTH0_DOMAIN}
      - VITE_AUTH0_CLIENT_ID=${VITE_AUTH0_CLIENT_ID}
    depends_on:
      - backend
    ports:
      - "5173:5173"

volumes:
  postgres_data:
```

---

## 🔧 Services

### 1. Database (PostgreSQL)

**Configuration**:
```yaml
db:
  image: postgres:15-alpine
  container_name: financial_db
  volumes:
    - postgres_data:/var/lib/postgresql/data
  environment:
    - POSTGRES_USER=${POSTGRES_USER:-postgres}
    - POSTGRES_PASSWORD=${POSTGRES_PASSWORD:-postgres}
    - POSTGRES_DB=${POSTGRES_DB:-financial_db}
  ports:
    - "5432:5432"
```

**Features**:
- Image: `postgres:15-alpine` (lightweight)
- Port: 5432 (accessible from host)
- Volume: `postgres_data` (persistent)
- Credentials: From environment variables

**Useful Commands**:
```bash
# Access PostgreSQL shell
docker-compose exec db psql -U postgres -d financial_db

# View logs
docker-compose logs -f db

# Backup
docker-compose exec db pg_dump -U postgres financial_db > backup.sql

# Restore
docker-compose exec -T db psql -U postgres financial_db < backup.sql
```

### 2. Backend (FastAPI)

**Configuration**:
```yaml
backend:
  build:
    context: ./backend
    dockerfile: Dockerfile
  container_name: financial_backend
  volumes:
    - ./backend:/app  # Hot reload enabled
  environment:
    - POSTGRES_SERVER=db  # DB service name
    - AUTH0_DOMAIN=${AUTH0_DOMAIN}
    - SECRET_KEY=${SECRET_KEY}
  depends_on:
    - db
  ports:
    - "8000:8000"
  command: ./scripts/start.sh
```

**Features**:
- Build: Custom Dockerfile
- Port: 8000
- Hot Reload: ✅ (mounted volume)
- Migrations: Auto-executed at startup
- Health Check: `/api/v1/health`

**Useful Commands**:
```bash
# View logs
docker-compose logs -f backend

# Access shell
docker-compose exec backend bash

# Execute migrations manually
docker-compose exec backend alembic upgrade head

# Create new migration
docker-compose exec backend alembic revision --autogenerate -m "description"

# Execute Python commands
docker-compose exec backend python -c "print('Hello')"

# Restart backend only
docker-compose restart backend
```

### 3. Frontend (React)

**Configuration**:
```yaml
frontend:
  build:
    context: ./frontend
    dockerfile: Dockerfile
    target: development-dependencies-env
  container_name: financial_frontend
  volumes:
    - ./frontend:/app
    - /app/node_modules  # Internal node_modules
  environment:
    - VITE_API_URL=${VITE_API_URL:-http://localhost:8000/api/v1}
    - VITE_AUTH0_DOMAIN=${VITE_AUTH0_DOMAIN}
    - VITE_AUTH0_CLIENT_ID=${VITE_AUTH0_CLIENT_ID}
  depends_on:
    - backend
  ports:
    - "5173:5173"
  command: npm run dev
```

**Features**:
- Build: Multi-stage Dockerfile
- Port: 5173 (Vite)
- Hot Reload: ✅ (mounted volume)
- Node Modules: Internal to container

**Useful Commands**:
```bash
# View logs
docker-compose logs -f frontend

# Access shell
docker-compose exec frontend sh

# Install dependency
docker-compose exec frontend npm install package-name

# Production build
docker-compose exec frontend npm run build

# Restart frontend only
docker-compose restart frontend
```

---

## 🔐 Environment Variables

### Complete `.env` File

```env
# ========================================
# Database Configuration
# ========================================
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_DB=financial_db

# ========================================
# Auth0 Configuration
# ========================================
AUTH0_DOMAIN=your-tenant.auth0.com
AUTH0_AUDIENCE=https://your-api-audience.com

# ========================================
# Backend Security
# ========================================
# Generate with: openssl rand -hex 32
SECRET_KEY=your_secret_key_here_change_in_production

# ========================================
# Frontend Auth0 Configuration
# ========================================
VITE_AUTH0_DOMAIN=your-tenant.auth0.com
VITE_AUTH0_CLIENT_ID=your_auth0_client_id
VITE_AUTH0_AUDIENCE=https://your-api-audience.com
VITE_AUTH0_REDIRECT_URI=http://localhost:5173/callback

# ========================================
# Optional - API URL
# ========================================
VITE_API_URL=http://localhost:8000/api/v1
```

### Default Values

In `docker-compose.yml`, you can use default values:

```yaml
environment:
  - POSTGRES_USER=${POSTGRES_USER:-postgres}  # Default: postgres
  - POSTGRES_PASSWORD=${POSTGRES_PASSWORD:-postgres}
  - VITE_API_URL=${VITE_API_URL:-http://localhost:8000/api/v1}
```

### Verify Variables

```bash
# View final configuration with resolved variables
docker-compose config

# View variables for a specific service
docker-compose exec backend env | grep AUTH0
```

---

## 💾 Volumes and Persistence

### Defined Volumes

```yaml
volumes:
  postgres_data:  # PostgreSQL data
```

### Mount Types

**1. Named Volume** (PostgreSQL):
```yaml
db:
  volumes:
    - postgres_data:/var/lib/postgresql/data
```
- Persistent data between restarts
- Managed by Docker
- Survives `docker-compose down`

**2. Bind Mount** (Backend and Frontend):
```yaml
backend:
  volumes:
    - ./backend:/app  # Local code → container
```
- Hot reload enabled
- Local changes reflected immediately

**3. Anonymous Volume** (node_modules):
```yaml
frontend:
  volumes:
    - /app/node_modules  # Protect internal node_modules
```
- Prevents local node_modules from overwriting container's

### Volume Commands

```bash
# List volumes
docker volume ls

# Inspect volume
docker volume inspect financial-dashboard_postgres_data

# View volume location
docker volume inspect financial-dashboard_postgres_data --format '{{ .Mountpoint }}'

# Delete volume (⚠️ deletes data)
docker volume rm financial-dashboard_postgres_data

# Delete unused volumes
docker volume prune
```

### Backup and Restore

**PostgreSQL Backup**:
```bash
# Create backup
docker-compose exec db pg_dump -U postgres financial_db > backup_$(date +%Y%m%d).sql

# Or with docker run
docker run --rm --volumes-from financial_db \
  -v $(pwd):/backup postgres:15-alpine \
  pg_dump -U postgres financial_db > /backup/backup.sql
```

**Restore**:
```bash
# From local file
docker-compose exec -T db psql -U postgres financial_db < backup.sql

# Reset DB and restore
docker-compose exec db psql -U postgres -c "DROP DATABASE financial_db;"
docker-compose exec db psql -U postgres -c "CREATE DATABASE financial_db OWNER postgres;"
docker-compose exec -T db psql -U postgres financial_db < backup.sql
```

---

## 🌐 Networking

### Default Network

Docker Compose creates a network automatically:
```
financial-dashboard_default
```

### Inter-Service Communication

Services communicate by name:

```python
# Backend connects to DB using service name
POSTGRES_SERVER=db  # ← Service name, not "localhost"

# Frontend connects to backend
VITE_API_URL=http://backend:8000/api/v1  # Inside Docker
VITE_API_URL=http://localhost:8000/api/v1  # From browser (host)
```

### Exposed Ports

```yaml
ports:
  - "host:container"
  - "5432:5432"  # PostgreSQL
  - "8000:8000"  # Backend
  - "5173:5173"  # Frontend
```

### Inspect Network

```bash
# List networks
docker network ls

# Inspect network
docker network inspect financial-dashboard_default

# View container IPs
docker-compose exec backend ping db
```

---

## 🛠️ Useful Commands

### Lifecycle Management

```bash
# Start everything
docker-compose up

# Start in background
docker-compose up -d

# Start and rebuild
docker-compose up --build

# Stop everything
docker-compose down

# Stop and remove volumes (⚠️ deletes DB)
docker-compose down -v

# Pause services
docker-compose pause

# Resume services
docker-compose unpause
```

### Individual Services

```bash
# Start backend only (and its dependencies)
docker-compose up backend

# Restart frontend only
docker-compose restart frontend

# Stop db only
docker-compose stop db

# View backend logs
docker-compose logs -f backend

# View all service logs
docker-compose logs -f

# View last 100 lines
docker-compose logs --tail=100
```

### Execute Commands

```bash
# Execute command in running container
docker-compose exec backend bash
docker-compose exec frontend sh
docker-compose exec db psql -U postgres

# Execute one-off command
docker-compose run --rm backend python -c "print('Hello')"
docker-compose run --rm frontend npm install
```

### Status and Debug

```bash
# View service status
docker-compose ps

# View resource usage
docker stats

# Inspect service
docker-compose exec backend env

# View final configuration
docker-compose config
```

### Cleanup

```bash
# Remove stopped containers
docker-compose down

# Remove unused images
docker image prune

# Remove everything (containers, networks, volumes, images)
docker system prune -a --volumes

# Rebuild from scratch
docker-compose down -v
docker-compose build --no-cache
docker-compose up
```

---

## 🐛 Troubleshooting

### Error: "Cannot connect to Docker daemon"

```bash
# Verify Docker Desktop is running
# macOS: Open Docker Desktop app

# Linux: Start Docker daemon
sudo systemctl start docker

# Verify
docker ps
```

### Error: "Port is already in use"

```bash
# See which process uses the port
lsof -i :8000  # Backend
lsof -i :5173  # Frontend
lsof -i :5432  # PostgreSQL

# Option 1: Kill the process
kill -9 <PID>

# Option 2: Change port in docker-compose.yml
ports:
  - "8001:8000"  # Host:Container
```

### Error: "Database connection refused"

```bash
# Verify DB container is running
docker-compose ps db

# View DB logs
docker-compose logs db

# Verify backend uses correct name
docker-compose exec backend env | grep POSTGRES_SERVER
# Should be: POSTGRES_SERVER=db
```

### Error: Hot Reload Not Working

```bash
# Verify volumes are mounted
docker-compose config | grep volumes

# Restart with rebuild
docker-compose down
docker-compose up --build

# macOS: Verify File Sharing in Docker Desktop
# Settings → Resources → File Sharing
```

### Error: "Out of disk space"

```bash
# View space usage
docker system df

# Clean unused images
docker image prune -a

# Clean unused volumes
docker volume prune

# Clean everything
docker system prune -a --volumes
```

### Container Constantly Restarting

```bash
# View logs to identify error
docker-compose logs backend

# View last lines before crash
docker-compose logs --tail=50 backend

# View exit code
docker-compose ps
```

### Environment Variables Not Loading

```bash
# Verify .env exists
ls -la .env

# View final configuration
docker-compose config

# Restart services after editing .env
docker-compose down
docker-compose up
```

---

## 🚀 Production

### docker-compose.prod.yml

Create file for production:

```yaml
version: '3.8'

services:
  db:
    restart: always
    environment:
      - POSTGRES_PASSWORD=${POSTGRES_PASSWORD}  # From secrets

  backend:
    build:
      context: ./backend
      target: production
    restart: always
    environment:
      - ENVIRONMENT=production
      - DEBUG=False
    command: uvicorn src.main:app --host 0.0.0.0 --port 8000

  frontend:
    build:
      context: ./frontend
      target: production
    restart: always
    command: npm run preview

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
      - ./ssl:/etc/nginx/ssl
    depends_on:
      - backend
      - frontend
```

### Use Production Compose

```bash
# Start with production config
docker-compose -f docker-compose.prod.yml up -d

# Production build
docker-compose -f docker-compose.prod.yml build --no-cache

# View logs
docker-compose -f docker-compose.prod.yml logs -f
```

### Secrets Management

**Option 1: Docker Secrets** (Swarm mode):
```yaml
secrets:
  postgres_password:
    external: true

services:
  db:
    secrets:
      - postgres_password
```

**Option 2: System Environment Variables**:
```bash
export POSTGRES_PASSWORD=secure_password
docker-compose up
```

**Option 3: .env.production**:
```bash
# DO NOT commit to git
.env.production
```

---

## 📚 Additional Resources

### Official Documentation
- [Docker Docs](https://docs.docker.com/)
- [Docker Compose Reference](https://docs.docker.com/compose/compose-file/)
- [Docker Best Practices](https://docs.docker.com/develop/dev-best-practices/)

### Reference Commands

```bash
# View all docker-compose options
docker-compose --help

# View help for a specific command
docker-compose up --help
```

---

## ✅ Setup Completion Checklist

- [ ] Docker Desktop installed and running
- [ ] Repository cloned
- [ ] `.env` file configured with all variables
- [ ] `docker-compose up` executed successfully
- [ ] All 3 services are running (db, backend, frontend)
- [ ] Frontend accessible at http://localhost:5173
- [ ] Backend accessible at http://localhost:8000
- [ ] API Docs accessible at http://localhost:8000/docs
- [ ] Hot reload works (code changes are reflected)

---

**Ready to develop with Docker! 🐳**
