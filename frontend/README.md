# ⚛️ Frontend - Financial Dashboard

React 19 application with TypeScript, React Router 7, and TanStack Query.

---

## 🏗️ Architecture

```text
frontend/app/
├── routes/          # React Router pages
├── features/        # Feature modules (auth, portfolio)
├── widgets/         # Composite UI components
├── entities/        # Domain models & queries
├── shared/          # Shared utilities & UI components
└── root.tsx         # App root
```

**Architecture Pattern**: Feature-Sliced Design

**Full Documentation**: [../docs/ARCHITECTURE.md](../docs/ARCHITECTURE.md)

---

## 🚀 Quick Start

### Docker (Recommended)

```bash
docker-compose up -d
# Access: http://localhost:5173
```

### Local Development

```bash
cd frontend
npm install
npm run dev
# Access: http://localhost:5173
```

**Setup Guide**: [../docs/FRONTEND_SETUP.md](../docs/FRONTEND_SETUP.md)

---

## 📚 Documentation

- [Frontend Setup Guide](../docs/FRONTEND_SETUP.md)
- [Architecture Overview](../docs/ARCHITECTURE.md)
- [Docker Guide](../docs/DOCKER_GUIDE.md)
- [Auth0 Configuration](../docs/FRONTEND_SETUP.md#auth0-configuration)
