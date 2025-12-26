# ⚛️ Frontend Setup Guide - Financial Dashboard

**Stack**: React 19 + TypeScript + Vite + React Router 7

---

## 📋 Table of Contents

1. [Prerequisites](#prerequisites)
2. [Option 1: Docker Development](#option-1-docker-development-recommended)
3. [Option 2: Local Development](#option-2-local-development)
4. [Environment Variables Configuration](#environment-variables-configuration)
5. [Project Structure](#project-structure)
6. [Useful Commands](#useful-commands)
7. [Auth0 Configuration](#auth0-configuration)
8. [Troubleshooting](#troubleshooting)

---

## 📦 Prerequisites

### For Docker Development
- **Docker Desktop** (includes Docker Compose)
- **Git**

### For Local Development
- **Node.js 20+** (recommended: use nvm)
- **npm** or **yarn**
- **Git**

---

## 🐳 Option 1: Docker Development (Recommended)

### Step 1: Clone the Repository

```bash
git clone <repository-url>
cd financial-dashboard
```

### Step 2: Configure Environment Variables

```bash
# Copy the example file
cp .env.example .env

# Edit with your values
nano .env
```

**Minimum required configuration**:
```env
# Auth0 (obtain from https://manage.auth0.com)
VITE_AUTH0_DOMAIN=your-tenant.auth0.com
VITE_AUTH0_CLIENT_ID=your_client_id
VITE_AUTH0_AUDIENCE=https://your-api-audience.com
VITE_AUTH0_REDIRECT_URI=http://localhost:5173/callback

# API URL
VITE_API_URL=http://localhost:8000/api/v1
```

### Step 3: Start the Services

```bash
# Build and start all services
docker-compose up --build

# Or just the frontend and its dependencies
docker-compose up frontend
```

This will start:
- ✅ Frontend (Vite) on port **5173**
- ✅ Backend (FastAPI) on port **8000**
- ✅ PostgreSQL on port **5432**

### Step 4: Verify the Frontend is Running

```bash
# View frontend logs
docker-compose logs -f frontend

# Should display:
# VITE v5.x.x  ready in XXX ms
# ➜  Local:   http://localhost:5173/
```

Access:
- **Frontend**: http://localhost:5173

### Step 5: Development with Hot Reload

The code is mounted as a volume, changes are reflected automatically:

```bash
# Edit any file in frontend/app/
# Vite will automatically reload the browser
```

### Useful Docker Commands

```bash
# View status
docker-compose ps

# View frontend logs
docker-compose logs -f frontend

# Restart frontend
docker-compose restart frontend

# Stop everything
docker-compose down

# Access the container shell
docker-compose exec frontend sh

# Install new dependency
docker-compose exec frontend npm install package-name

# Run build
docker-compose exec frontend npm run build
```

---

## 💻 Option 2: Local Development

### Step 1: Install Node.js

**Using nvm (recommended)**:
```bash
# Install nvm
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.0/install.sh | bash

# Install Node.js 20
nvm install 20
nvm use 20
nvm alias default 20

# Verify version
node --version  # Should be v20.x.x
npm --version
```

**macOS (Homebrew)**:
```bash
brew install node@20
```

**Windows**:
- Download from https://nodejs.org/

### Step 2: Configure Environment Variables

```bash
cd frontend

# Copy example file
cp .env.example .env

# Edit with your values
nano .env
```

**`.env` File**:
```env
# API URL - Should point to running backend
VITE_API_URL=http://localhost:8000/api/v1

# Auth0 Configuration
VITE_AUTH0_DOMAIN=your-tenant.auth0.com
VITE_AUTH0_CLIENT_ID=your_auth0_client_id
VITE_AUTH0_AUDIENCE=https://your-api-audience.com
VITE_AUTH0_REDIRECT_URI=http://localhost:5173/callback
```

### Step 3: Install Dependencies

```bash
cd frontend

# With npm
npm install

# Or with yarn
yarn install
```

### Step 4: Start the Development Server

```bash
# With npm
npm run dev

# Or with yarn
yarn dev
```

The frontend will be available at:
- **Local**: http://localhost:5173

### Local Development - Useful Commands

```bash
cd frontend

# Install dependencies
npm install

# Development mode (hot reload)
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview

# Linter
npm run lint

# Auto-fix lint issues
npm run lint:fix

# Type checking
npm run type-check

# Install new dependency
npm install package-name

# Install dev dependency
npm install -D package-name

# Update dependencies
npm update

# List outdated dependencies
npm outdated
```

---

## 🔧 Environment Variables Configuration

### Available Variables

```env
# ========================================
# API Configuration
# ========================================
VITE_API_URL=http://localhost:8000/api/v1

# ========================================
# Auth0 Configuration
# ========================================
# Your Auth0 tenant domain
VITE_AUTH0_DOMAIN=your-tenant.auth0.com

# Your application Client ID in Auth0
VITE_AUTH0_CLIENT_ID=your_client_id_here

# Your API audience
VITE_AUTH0_AUDIENCE=https://your-api-audience.com

# Callback URL after login
VITE_AUTH0_REDIRECT_URI=http://localhost:5173/callback

# ========================================
# Optional: Feature Flags
# ========================================
VITE_ENABLE_ANALYTICS=false
VITE_ENABLE_DEBUG=true
```

### Accessing Variables in Code

```typescript
// ✅ CORRECT - Variables with VITE_ prefix
const apiUrl = import.meta.env.VITE_API_URL;
const auth0Domain = import.meta.env.VITE_AUTH0_DOMAIN;

// ❌ INCORRECT - Without VITE_ prefix
const secret = import.meta.env.SECRET_KEY;  // undefined
```

### Different Environments

```bash
# Development
.env                    # Local variables

# Production
.env.production         # Production variables
```

Load production variables:
```bash
npm run build  # Uses .env.production automatically
```

---

## 📁 Project Structure

```
frontend/
├── app/                          # Source code
│   ├── routes/                   # React Router pages
│   │   ├── index.tsx             # Landing page
│   │   ├── callback.tsx          # Auth0 callback
│   │   ├── dashboard.tsx         # Dashboard layout
│   │   └── dashboard.portfolio.tsx
│   │
│   ├── features/                 # Feature modules
│   │   ├── auth/                 # Authentication
│   │   │   └── components/
│   │   │       ├── ProtectedRoute.tsx
│   │   │       └── DashboardSkeleton.tsx
│   │   │
│   │   ├── portfolio/            # Portfolio features
│   │   │   ├── components/
│   │   │   │   ├── UploadPortfolio.tsx
│   │   │   │   ├── BulkUploadPortfolio.tsx
│   │   │   │   └── SnapshotHistory.tsx
│   │   │   └── api/
│   │   │       └── uploadPortfolio.ts
│   │   │
│   │   └── health/               # Health check
│   │
│   ├── widgets/                  # UI composite widgets
│   │   ├── portfolio-stats/
│   │   │   └── ui/
│   │   │       └── PortfolioStats.tsx
│   │   ├── holdings-table/
│   │   └── history-chart/
│   │
│   ├── entities/                 # Domain models
│   │   ├── holding/
│   │   │   └── api/
│   │   │       └── queries.ts
│   │   └── portfolio/
│   │
│   ├── shared/                   # Shared utilities
│   │   ├── api/
│   │   │   └── client.ts         # Axios instance
│   │   ├── hooks/
│   │   │   └── useAuthenticatedClient.ts
│   │   ├── lib/
│   │   │   ├── auth-utils.ts
│   │   │   └── auth-storage.ts
│   │   ├── stores/
│   │   │   └── auth-store.ts     # Zustand store
│   │   └── ui/                   # UI components
│   │       ├── button.tsx
│   │       ├── card.tsx
│   │       └── skeleton.tsx
│   │
│   ├── root.tsx                  # App root
│   └── routes.ts                 # Routes config
│
├── public/                       # Static assets
├── .env.example                  # Env variables template
├── Dockerfile                    # Docker config
├── package.json                  # Dependencies
├── tsconfig.json                 # TypeScript config
├── tailwind.config.ts            # Tailwind config
└── vite.config.ts                # Vite config
```

### Organization by Layers (Feature-Sliced Design)

```
app/
├── routes/      # Pages (routes)
├── features/    # Business logic per feature
├── widgets/     # Composite UI components
├── entities/    # Domain models
└── shared/      # Shared utilities
```

---

## 🎨 Useful Commands

### Development

```bash
# Start development server
npm run dev

# Build for production
npm run build

# Preview build
npm run preview

# Clean cache and node_modules
rm -rf node_modules package-lock.json
npm install
```

### Linting and Formatting

```bash
# Run ESLint
npm run lint

# Auto-fix
npm run lint:fix

# Format with Prettier (if configured)
npm run format
```

### Type Checking

```bash
# Verify TypeScript types
npm run type-check

# Watch mode
tsc --watch
```

### Dependencies

```bash
# Install new dependency
npm install axios

# Install dev dependency
npm install -D @types/node

# Uninstall dependency
npm uninstall axios

# Update all dependencies
npm update

# Check vulnerabilities
npm audit

# Fix vulnerabilities
npm audit fix
```

### Testing (if configured)

```bash
# Run tests
npm run test

# Watch mode
npm run test:watch

# Coverage
npm run test:coverage
```

---

## 🔐 Auth0 Configuration

### Step 1: Create Application in Auth0

1. Go to https://manage.auth0.com
2. Navigate to **Applications** → **Create Application**
3. Name: "Financial Dashboard"
4. Type: **Single Page Application**
5. Click **Create**

### Step 2: Configure the Application

In the **Settings** tab:

```
Allowed Callback URLs:
http://localhost:5173/callback
https://your-domain.com/callback

Allowed Logout URLs:
http://localhost:5173
https://your-domain.com

Allowed Web Origins:
http://localhost:5173
https://your-domain.com

Allowed Origins (CORS):
http://localhost:5173
https://your-domain.com
```

Click **Save Changes**

### Step 3: Create API in Auth0

1. Navigate to **Applications** → **APIs** → **Create API**
2. Name: "Financial Dashboard API"
3. Identifier: `https://api.financial-dashboard.com`
   (This is your **Audience**)
4. Signing Algorithm: RS256
5. Click **Create**

### Step 4: Copy Credentials

From the created application, copy:
- **Domain**: `your-tenant.auth0.com`
- **Client ID**: `abc123...`

From the created API, copy:
- **Identifier** (Audience): `https://api.financial-dashboard.com`

### Step 5: Configure in `.env`

```env
VITE_AUTH0_DOMAIN=your-tenant.auth0.com
VITE_AUTH0_CLIENT_ID=abc123xyz456...
VITE_AUTH0_AUDIENCE=https://api.financial-dashboard.com
VITE_AUTH0_REDIRECT_URI=http://localhost:5173/callback
```

### Step 6: Restart the Server

```bash
# Stop the server (Ctrl+C)
# Restart
npm run dev
```

---

## 🎨 UI Customization

### Tailwind CSS

Configure colors, fonts, etc. in `tailwind.config.ts`:

```typescript
export default {
  theme: {
    extend: {
      colors: {
        primary: {
          50: '#f0f9ff',
          500: '#0ea5e9',
          900: '#0c4a6e',
        },
      },
    },
  },
}
```

### UI Components

Base components are in `app/shared/ui/`:

```typescript
import { Button } from "~/shared/ui/button"
import { Card } from "~/shared/ui/card"
import { Skeleton } from "~/shared/ui/skeleton"
```

---

## 📦 Adding New Dependencies

### Example: Adding date-fns

```bash
# Install
npm install date-fns

# Use in code
import { format } from 'date-fns';

const formattedDate = format(new Date(), 'yyyy-MM-dd');
```

### Example: Adding Chart.js

```bash
# Install
npm install chart.js react-chartjs-2

# Use in component
import { Line } from 'react-chartjs-2';
```

---

## 🐛 Troubleshooting

### Error: "Module not found"

```bash
# Clean node_modules and reinstall
rm -rf node_modules package-lock.json
npm install
```

### Error: "VITE_* variable is undefined"

```bash
# Verify .env exists
ls -la frontend/.env

# Verify content
cat frontend/.env

# Restart server
npm run dev
```

### Error: "Port 5173 is already in use"

```bash
# See which process is using the port
lsof -i :5173

# Kill the process
kill -9 <PID>

# Or use another port
npm run dev -- --port 3000
```

### Error: Auth0 "Invalid state"

```bash
# Clear localStorage
# In DevTools → Application → Local Storage → Clear

# Verify callback URL in Auth0
# Must match exactly with VITE_AUTH0_REDIRECT_URI
```

### Error: CORS on API requests

```bash
# Verify VITE_API_URL in .env
cat frontend/.env | grep VITE_API_URL

# Verify BACKEND_CORS_ORIGINS in backend
cat backend/.env | grep CORS

# Should include: http://localhost:5173
```

### Hot Reload Not Working

```bash
# With Docker: Verify volume
docker-compose config | grep frontend

# Restart container
docker-compose restart frontend

# Local: Clean Vite cache
rm -rf node_modules/.vite
npm run dev
```

### TypeScript Errors

```bash
# Verify types
npm run type-check

# Regenerate node_modules types
rm -rf node_modules
npm install
```

### Build Fails in Production

```bash
# View detailed errors
npm run build -- --debug

# Verify all env vars are in .env.production
cat .env.production

# Clean dist
rm -rf dist
npm run build
```

---

## 📚 Additional Resources

### Official Documentation
- [React 19](https://react.dev)
- [React Router 7](https://reactrouter.com)
- [Vite](https://vitejs.dev)
- [TypeScript](https://www.typescriptlang.org)
- [Tailwind CSS](https://tailwindcss.com)
- [TanStack Query](https://tanstack.com/query/latest)
- [Auth0 React SDK](https://auth0.com/docs/quickstart/spa/react)

### Tutorials
- [React Router Tutorial](https://reactrouter.com/en/main/start/tutorial)
- [TanStack Query Tutorial](https://tanstack.com/query/latest/docs/react/quick-start)

---

## ✅ Setup Completion Checklist

- [ ] Node.js 20+ installed
- [ ] Repository cloned
- [ ] `.env` file configured
- [ ] Dependencies installed (`npm install`)
- [ ] Auth0 application created
- [ ] Auth0 credentials in `.env`
- [ ] Frontend running at http://localhost:5173
- [ ] Backend running at http://localhost:8000
- [ ] Login with Auth0 works

---

**Ready to develop! 🎨**
