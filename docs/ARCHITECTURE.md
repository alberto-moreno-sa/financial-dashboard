# 🏗️ System Architecture - Financial Dashboard

**Last Updated**: 2025-12-29
**Version**: 1.0.0

---

## 📋 Table of Contents

1. [Overview](#overview)
2. [Technology Stack](#technology-stack)
3. [High-Level Architecture](#high-level-architecture)
4. [Project Structure](#project-structure)
5. [Core Components](#core-components)
6. [Data Flow](#data-flow)
7. [Authentication and Authorization](#authentication-and-authorization)
8. [Database](#database)
9. [API Endpoints](#api-endpoints)
10. [Design Patterns](#design-patterns)

---

## 🎯 Overview

Financial Dashboard is a complete investment portfolio management system that allows users to:
- Upload GBM account statements in PDF format
- Visualize their current portfolio and historical evolution
- Analyze individual positions and returns
- Manage multiple monthly snapshots

### Key Features
- ✅ Authentication with Auth0
- ✅ Individual and bulk PDF uploads (up to 100 files)
- ✅ Automatic duplicate detection
- ✅ Intelligent GBM document parsing
- ✅ Real-time data visualization
- ✅ Multi-tenant per user

---

## 🚀 Technology Stack

### Backend
```
Python 3.11
├── FastAPI (Async web framework)
├── SQLAlchemy 2.0 (Async ORM)
├── Alembic (Migrations)
├── Pydantic V2 (Validation)
├── pdfplumber (PDF parsing)
├── Auth0 (Authentication)
└── AsyncPG (PostgreSQL driver)
```

### Frontend
```
TypeScript + React 19
├── React Router 7 (Routing)
├── TanStack Query (Async state management)
├── Zustand (Global state management)
├── Tailwind CSS v4 (Styling)
├── Radix UI (Components)
├── Recharts (Charts)
└── Auth0 React SDK (Authentication)
```

### Infrastructure
```
Docker + Docker Compose
├── PostgreSQL 15 (Database)
├── Backend Container (FastAPI)
└── Frontend Container (Vite dev server)
```

---

## 🏛️ High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                            USER                                 │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│                   AUTH0 (Authentication)                        │
│  - Login/Logout                                                 │
│  - JWT Token Management                                         │
│  - User Profile                                                 │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│                    FRONTEND (React 19)                          │
│                                                                 │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐         │
│  │   Features   │  │   Widgets    │  │   Entities   │         │
│  │  (Business)  │  │    (UI)      │  │   (Models)   │         │
│  └──────────────┘  └──────────────┘  └──────────────┘         │
│                                                                 │
│  ┌──────────────────────────────────────────────────────┐     │
│  │              TanStack Query (Cache)                   │     │
│  └──────────────────────────────────────────────────────┘     │
└────────────────────────┬────────────────────────────────────────┘
                         │ HTTP + JWT
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│                    BACKEND (FastAPI)                            │
│                                                                 │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐         │
│  │  API Routes  │→ │   Services   │→ │   Models     │         │
│  │  (v1/*)      │  │  (Business)  │  │  (ORM)       │         │
│  └──────────────┘  └──────────────┘  └──────────────┘         │
│                                                                 │
│  ┌──────────────────────────────────────────────────────┐     │
│  │         Auth0 JWT Validation Middleware              │     │
│  └──────────────────────────────────────────────────────┘     │
└────────────────────────┬────────────────────────────────────────┘
                         │ SQL (AsyncPG)
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│                   DATABASE (PostgreSQL 15)                      │
│                                                                 │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐      │
│  │  Users   │  │Portfolio │  │Snapshots │  │ Upload   │      │
│  │          │  │          │  │          │  │ History  │      │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘      │
└─────────────────────────────────────────────────────────────────┘
```

---

## 📁 Project Structure

```
financial-dashboard/
│
├── backend/                      # FastAPI Backend
│   ├── src/
│   │   ├── api/
│   │   │   └── v1/              # API endpoints v1
│   │   │       ├── auth.py      # Authentication
│   │   │       ├── users.py     # User management
│   │   │       ├── portfolio.py # Portfolio endpoints
│   │   │       ├── import_data.py # Upload and bulk upload
│   │   │       └── health.py    # Health checks
│   │   │
│   │   ├── core/                # Core configuration
│   │   │   ├── config.py        # Settings
│   │   │   ├── database.py      # DB connection
│   │   │   ├── auth0.py         # Auth0 config
│   │   │   └── security.py      # JWT utilities
│   │   │
│   │   ├── models/              # SQLAlchemy models
│   │   │   ├── user.py
│   │   │   ├── portfolio.py
│   │   │   └── snapshot.py
│   │   │
│   │   ├── schemas/             # Pydantic schemas
│   │   │   ├── user.py
│   │   │   ├── portfolio.py
│   │   │   └── import_data.py
│   │   │
│   │   ├── services/            # Business logic
│   │   │   ├── pdf_parser.py    # PDF parsing
│   │   │   ├── snapshot_service.py
│   │   │   └── analytics.py
│   │   │
│   │   └── main.py             # App entry point
│   │
│   ├── migrations/              # Alembic migrations
│   ├── Dockerfile
│   ├── pyproject.toml          # Poetry dependencies
│   └── .env.example
│
├── frontend/                    # React Frontend
│   ├── app/
│   │   ├── routes/             # React Router pages
│   │   │   ├── index.tsx       # Landing
│   │   │   ├── callback.tsx    # Auth callback
│   │   │   ├── dashboard.tsx   # Dashboard layout
│   │   │   └── dashboard.portfolio.tsx
│   │   │
│   │   ├── features/           # Feature modules
│   │   │   ├── auth/           # Auth components
│   │   │   ├── portfolio/      # Portfolio features
│   │   │   │   ├── components/
│   │   │   │   │   ├── UploadPortfolio.tsx
│   │   │   │   │   ├── BulkUploadPortfolio.tsx
│   │   │   │   │   └── SnapshotHistory.tsx
│   │   │   │   └── api/
│   │   │   │       └── uploadPortfolio.ts
│   │   │   └── health/
│   │   │
│   │   ├── widgets/            # UI composite widgets
│   │   │   ├── portfolio-stats/
│   │   │   ├── holdings-table/
│   │   │   └── history-chart/
│   │   │
│   │   ├── entities/           # Domain models
│   │   │   ├── holding/
│   │   │   └── portfolio/
│   │   │
│   │   ├── shared/             # Shared utilities
│   │   │   ├── api/            # API client
│   │   │   ├── hooks/          # Custom hooks
│   │   │   ├── lib/            # Utilities
│   │   │   ├── stores/         # Zustand stores
│   │   │   └── ui/             # UI components
│   │   │
│   │   └── root.tsx            # App root
│   │
│   ├── Dockerfile
│   ├── package.json
│   └── .env.example
│
├── docs/                        # Documentation
│   ├── ARCHITECTURE.md         # This file
│   ├── BACKEND_SETUP.md
│   └── FRONTEND_SETUP.md
│
├── docker-compose.yml          # Orchestration
├── .env.example               # Environment variables
└── README.md                  # Main documentation
```

---

## 🔧 Core Components

### 1. Authentication System (Auth0)

**Authentication Flow**:
```
1. User → Click "Login"
2. Redirect → Auth0 Universal Login
3. User → Enter credentials
4. Auth0 → Validates and generates JWT
5. Redirect → /callback with token
6. Frontend → Saves token in localStorage
7. Frontend → Makes requests with Authorization header
8. Backend → Validates JWT with Auth0
9. Backend → Extracts user info from token
10. Backend → Authorizes request
```

**Components**:
- `Auth0Provider` (Frontend): Context provider
- `useAuth0()` hook: Access to auth state
- `ProtectedRoute`: Route guard
- `auth0.py` (Backend): JWT validation
- `get_current_user()`: Dependency injection

### 2. Upload System

**Individual Upload**:
```python
POST /api/v1/import/upload
- Receives 1 PDF
- Parses content
- Checks duplicates (hash + date)
- Creates snapshot
- Returns result
```

**Bulk Upload**:
```python
POST /api/v1/import/bulk-upload
- Receives up to 100 PDFs
- Processes each file independently
- Handles errors per file
- Returns summary + details
```

**PDF Parser** (`pdf_parser.py`):
```python
class GBMStatementParser:
    - _extract_account_holder()
    - _extract_statement_date()
    - _find_value()  # RENTA VARIABLE, DEUDA, EFECTIVO
    - _extract_positions()  # Individual positions
```

### 3. Snapshot System

**Data Model**:
```
PortfolioSnapshot
├── id (UUID)
├── portfolio_id (FK → Portfolio)
├── user_id (FK → User)
├── snapshot_date (Date)
├── statement_period (String)
├── equity_value (Decimal)
├── fixed_income_value (Decimal)
├── cash_value (Decimal)
├── total_value (Decimal)
└── positions[] (One-to-Many → Position)

Position
├── id (UUID)
├── snapshot_id (FK → PortfolioSnapshot)
├── ticker (String)
├── name (String)
├── quantity (Integer)
├── avg_cost (Decimal)
├── current_price (Decimal)
├── market_value (Decimal)
├── unrealized_gain (Decimal)
└── unrealized_gain_percent (Decimal)
```

### 4. Cache System (Frontend)

**TanStack Query Keys**:
```typescript
["portfolio"]         // General portfolio
["holdings"]          // Current positions
["stats"]            // Statistics
["snapshot-history"] // Snapshot history
["transactions"]     // Transactions
```

**Automatic Invalidation**:
```typescript
// After successful upload
queryClient.invalidateQueries({ queryKey: ["portfolio"] });
queryClient.invalidateQueries({ queryKey: ["holdings"] });
queryClient.invalidateQueries({ queryKey: ["stats"] });
queryClient.invalidateQueries({ queryKey: ["snapshot-history"] });
```

---

## 📊 Data Flow

### Individual Upload Flow

```
1. User selects PDF
   ↓
2. Frontend: Validates file (type, size)
   ↓
3. POST /api/v1/import/upload
   ↓
4. Backend: Receives multipart/form-data
   ↓
5. Backend: Extracts user_id from JWT
   ↓
6. Backend: Reads binary file
   ↓
7. Backend: parse_gbm_pdf(content)
   ↓
8. Backend: Calculates SHA-256 hash
   ↓
9. Backend: check_duplicate_upload()
   ├─ If duplicate → 409 Conflict
   └─ If new → continue
   ↓
10. Backend: SnapshotService.create_snapshot()
    ├─ Creates PortfolioSnapshot
    ├─ Creates Positions[]
    ├─ Creates UploadHistory
    └─ db.commit()
   ↓
11. Frontend: Receives response
   ↓
12. Frontend: Invalidates queries
   ↓
13. Frontend: Dashboard updates automatically
```

### Bulk Upload Flow

```
1. User drags 100 PDFs
   ↓
2. Frontend: Validates (quantity, type)
   ↓
3. POST /api/v1/import/bulk-upload
   ↓
4. Backend: Receives FormData with files[]
   ↓
5. Backend: For each file:
   ├─ try:
   │   ├─ Parse PDF
   │   ├─ Check duplicate
   │   ├─ Create snapshot
   │   └─ result.status = "success"
   └─ except:
       └─ result.status = "error"
   ↓
6. Backend: Returns BulkUploadResponse
   {
     total_files: 100,
     successful: 95,
     duplicates: 3,
     errors: 2,
     results: [...]
   }
   ↓
7. Frontend: Shows results table
```

---

## 🔐 Authentication and Authorization

### Auth0 Configuration

**Tenant**: `dev-6gtndpthcg0k7461.us.auth0.com`
**Audience**: `https://api.financial-dashboard.com`

### JWT Structure
```json
{
  "sub": "google-oauth2|102985461173462510125",
  "email": "user@example.com",
  "email_verified": true,
  "name": "User Name",
  "picture": "https://...",
  "iss": "https://dev-6gtndpthcg0k7461.us.auth0.com/",
  "aud": "https://api.financial-dashboard.com",
  "iat": 1735483200,
  "exp": 1735569600
}
```

### Backend Validation

```python
from src.core.auth0 import verify_token

async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db)
) -> User:
    # 1. Validates JWT with Auth0
    payload = verify_token(token)

    # 2. Extracts auth0_id
    auth0_id = payload.get("sub")

    # 3. Finds/creates user
    user = await get_or_create_user(db, auth0_id, payload)

    return user
```

### Multi-Tenancy

All data is isolated by user:
```python
# Automatically filters by user_id
portfolio = await db.execute(
    select(Portfolio).where(Portfolio.user_id == current_user.id)
)
```

---

## 🗄️ Database

### Schema Overview

```sql
-- Users
CREATE TABLE users (
    id UUID PRIMARY KEY,
    auth0_id VARCHAR(255) UNIQUE NOT NULL,
    email VARCHAR(255) NOT NULL,
    name VARCHAR(255),
    picture VARCHAR(500),
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Portfolios (1 per user)
CREATE TABLE portfolios (
    id UUID PRIMARY KEY,
    user_id UUID REFERENCES users(id),
    name VARCHAR(255) DEFAULT 'My Portfolio',
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);

-- Monthly snapshots
CREATE TABLE portfolio_snapshots (
    id UUID PRIMARY KEY,
    portfolio_id UUID REFERENCES portfolios(id) ON DELETE CASCADE,
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    snapshot_date DATE NOT NULL,
    statement_period VARCHAR(50),
    equity_value DECIMAL(15,2),
    fixed_income_value DECIMAL(15,2),
    cash_value DECIMAL(15,2),
    total_value DECIMAL(15,2) NOT NULL,
    created_at TIMESTAMP,

    UNIQUE(portfolio_id, snapshot_date)
);

-- Individual positions
CREATE TABLE positions (
    id UUID PRIMARY KEY,
    snapshot_id UUID REFERENCES portfolio_snapshots(id) ON DELETE CASCADE,
    ticker VARCHAR(20) NOT NULL,
    name VARCHAR(255),
    quantity INTEGER NOT NULL,
    avg_cost DECIMAL(15,2),
    current_price DECIMAL(15,2),
    market_value DECIMAL(15,2) NOT NULL,
    unrealized_gain DECIMAL(15,2),
    unrealized_gain_percent DECIMAL(10,2),
    created_at TIMESTAMP
);

-- Upload history
CREATE TABLE upload_history (
    id UUID PRIMARY KEY,
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    portfolio_id UUID REFERENCES portfolios(id) ON DELETE CASCADE,
    snapshot_id UUID REFERENCES portfolio_snapshots(id) ON DELETE SET NULL,
    filename VARCHAR(255) NOT NULL,
    file_hash VARCHAR(64) NOT NULL,
    file_size INTEGER,
    statement_date DATE,
    upload_ip VARCHAR(45),
    uploaded_at TIMESTAMP DEFAULT NOW(),

    UNIQUE(user_id, file_hash, statement_date)
);
```

### Indexes

```sql
CREATE INDEX idx_snapshots_portfolio ON portfolio_snapshots(portfolio_id);
CREATE INDEX idx_snapshots_user ON portfolio_snapshots(user_id);
CREATE INDEX idx_snapshots_date ON portfolio_snapshots(snapshot_date);
CREATE INDEX idx_positions_snapshot ON positions(snapshot_id);
CREATE INDEX idx_upload_history_user ON upload_history(user_id);
CREATE INDEX idx_upload_history_hash ON upload_history(file_hash);
```

### Migrations (Alembic)

```bash
# Create migration
cd backend
alembic revision --autogenerate -m "description"

# Apply migrations
alembic upgrade head

# View history
alembic history
```

---

## 🌐 API Endpoints

### Authentication
```
POST   /api/v1/users/sync          # Sync Auth0 user
GET    /api/v1/users/me            # Get current user
```

### Portfolio
```
GET    /api/v1/portfolio/stats     # General statistics
GET    /api/v1/portfolio/holdings  # Current positions
GET    /api/v1/portfolio/transactions  # Transactions
```

### Dashboard
```
GET    /api/v1/portfolio/dashboard/stats  # Dashboard stats
```

### Import/Upload
```
POST   /api/v1/import/upload              # Individual upload
POST   /api/v1/import/bulk-upload         # Bulk upload (up to 100)
GET    /api/v1/import/history             # Upload history
GET    /api/v1/import/snapshot-history    # Snapshot history
```

### Health
```
GET    /api/v1/health                     # Health check
```

### Documentation
```
GET    /docs                              # Swagger UI
GET    /redoc                             # ReDoc
```

---

## 🎨 Design Patterns

### Backend Patterns

**1. Dependency Injection**
```python
async def create_snapshot(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # db and current_user are automatically injected
    pass
```

**2. Service Layer Pattern**
```python
# Separation of concerns
API Route → Service → Repository (ORM)
```

**3. Repository Pattern** (via SQLAlchemy)
```python
# Data access abstraction
result = await db.execute(select(Portfolio).where(...))
portfolio = result.scalar_one_or_none()
```

**4. DTO Pattern** (via Pydantic)
```python
class PortfolioStatsResponse(BaseModel):
    total_value: Decimal
    equity_percentage: float
    # ...
```

### Frontend Patterns

**1. Feature-Sliced Design**
```
features/     # Business logic features
widgets/      # Composite UI components
entities/     # Domain models
shared/       # Shared utilities
```

**2. Container/Presenter Pattern**
```typescript
// Container: Business logic
export function PortfolioStatsContainer() {
  const { data } = useQuery(["stats"], fetchStats);
  return <PortfolioStatsView data={data} />;
}

// Presenter: UI only
export function PortfolioStatsView({ data }) {
  return <div>...</div>;
}
```

**3. Custom Hooks**
```typescript
// Reusable logic encapsulation
function useAuthenticatedClient() {
  const { getAccessTokenSilently } = useAuth0();
  // ...
}
```

**4. Query Key Factory**
```typescript
const portfolioKeys = {
  all: ["portfolio"] as const,
  stats: () => [...portfolioKeys.all, "stats"] as const,
  holdings: () => [...portfolioKeys.all, "holdings"] as const,
};
```

---

## 🔄 Request Lifecycle

### Complete Request: PDF Upload

```
1. FRONTEND
   ↓
   User selects file
   ↓
   const formData = new FormData()
   formData.append("file", file)
   ↓
   const token = await getAccessTokenSilently()
   ↓
   axios.post("/import/upload", formData, {
     headers: { Authorization: `Bearer ${token}` }
   })

2. NETWORK
   ↓
   HTTP POST → http://localhost:8000/api/v1/import/upload
   Headers: {
     Authorization: Bearer eyJ...,
     Content-Type: multipart/form-data
   }

3. BACKEND - Middleware
   ↓
   CORS Middleware → Validates origin
   ↓
   Auth Middleware → Extracts token
   ↓
   verify_token(token) → Validates with Auth0
   ↓
   get_current_user() → Finds/creates user

4. BACKEND - Endpoint
   ↓
   @router.post("/upload")
   async def upload_statement(
     file: UploadFile,
     db: AsyncSession,
     current_user: User
   )
   ↓
   content = await file.read()
   ↓
   data = parse_gbm_pdf(content)

5. BACKEND - Business Logic
   ↓
   file_hash = hashlib.sha256(content).hexdigest()
   ↓
   duplicate = await check_duplicate_upload(...)
   if duplicate:
     raise HTTPException(409)
   ↓
   snapshot = await SnapshotService.create_snapshot(...)

6. BACKEND - Database
   ↓
   BEGIN TRANSACTION
   ↓
   INSERT INTO portfolio_snapshots ...
   INSERT INTO positions ...
   INSERT INTO upload_history ...
   ↓
   COMMIT

7. BACKEND - Response
   ↓
   return UploadResponse(
     snapshot_id=str(snapshot.id),
     snapshot_date=snapshot.snapshot_date,
     ...
   )

8. FRONTEND - Response Handling
   ↓
   onSuccess: (response) => {
     toast.success("Upload successful")
     queryClient.invalidateQueries(["portfolio"])
   }
   ↓
   Dashboard re-renders automatically
```

---

## 📈 Scalability and Performance

### Backend Optimizations

1. **Async/Await**: Entire backend is asynchronous
2. **Connection Pooling**: SQLAlchemy manages connection pool
3. **Eager Loading**: `selectinload()` to avoid N+1 queries
4. **Indexes**: On all FKs and search columns

### Frontend Optimizations

1. **React Query Cache**: Reduces redundant requests
2. **Code Splitting**: Per route (React Router)
3. **Lazy Loading**: Large components
4. **Debouncing**: In searches and filters

### Database Optimizations

1. **UUIDs**: For distributed IDs
2. **Partial Indexes**: On high cardinality columns
3. **EXPLAIN ANALYZE**: For slow queries
4. **Vacuum**: Automatic in PostgreSQL

---

## 🔒 Security

### Implemented Measures

1. ✅ JWT Validation with Auth0
2. ✅ CORS configured
3. ✅ SQL Injection prevention (ORM)
4. ✅ File upload validation
5. ✅ Multi-tenant isolation
6. ✅ HTTPS ready
7. ✅ Environment variables
8. ✅ No secrets in code

### Pending for Production

1. Rate Limiting
2. Request size limits
3. File type validation (magic numbers)
4. Secrets management (AWS Secrets Manager)
5. WAF (Web Application Firewall)
6. Monitoring and logging
7. Automated backup

---

## 📊 Monitoring and Logs

### Backend Logging
```python
# Structured logs
logger.info("Upload initiated", extra={
    "user_id": user.id,
    "filename": file.filename,
    "size": file.size
})
```

### Health Checks
```
GET /api/v1/health
{
  "status": "healthy",
  "database": "connected",
  "version": "1.0.0"
}
```

---

## 🚀 Deployment

### Required Environment Variables

```bash
# Database
POSTGRES_USER=postgres
POSTGRES_PASSWORD=***
POSTGRES_DB=financial_db

# Auth0
AUTH0_DOMAIN=your-tenant.auth0.com
AUTH0_AUDIENCE=https://your-api.com

# Security
SECRET_KEY=*** (generate with: openssl rand -hex 32)

# Frontend
VITE_AUTH0_DOMAIN=your-tenant.auth0.com
VITE_AUTH0_CLIENT_ID=***
VITE_AUTH0_AUDIENCE=https://your-api.com
```

### Docker Production

```yaml
# docker-compose.prod.yml
services:
  backend:
    environment:
      - ENVIRONMENT=production
      - DEBUG=False

  frontend:
    command: npm run build
```

---

## 📚 References

- [FastAPI Docs](https://fastapi.tiangolo.com)
- [React Router v7](https://reactrouter.com)
- [Auth0 Documentation](https://auth0.com/docs)
- [SQLAlchemy Async](https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html)
- [TanStack Query](https://tanstack.com/query/latest)

---

**End of Architecture Documentation**
