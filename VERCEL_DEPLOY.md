# 🚀 Vercel Deployment Guide - Demo Mode

Complete step-by-step guide to deploy Financial Dashboard on Vercel in **Demo Mode** (no authentication, in-memory storage).

---

## 📋 Prerequisites

- Vercel account (free tier works)
- GitHub account
- Project pushed to GitHub repository

---

## 🎯 Architecture Overview

**Frontend** (Vercel Project 1):
- React 19 + Vite
- Deployed as static site
- No authentication required in demo mode
- Redirects directly to dashboard

**Backend** (Vercel Project 2):
- FastAPI + Python
- Serverless functions
- In-memory storage (no database needed)
- Auto-resets on each deployment/restart

---

## 🔧 Step 1: Prepare Repository

1. **Ensure all files are committed**:
```bash
git status
git add .
git commit -m "Prepare for Vercel deployment"
git push origin main
```

2. **Verify .gitignore excludes sensitive files**:
```bash
cat .gitignore | grep -E "(\.env$|\.env\.production)"
```

Should show:
```
.env
.env.production
```

---

## 🎨 Step 2: Deploy Frontend to Vercel

### 2.1 Create Frontend Project

1. Go to https://vercel.com/new
2. Click "Import Project"
3. Select your GitHub repository
4. Configure project:

**Project Settings:**
```
Framework Preset: Vite
Root Directory: frontend
Build Command: npm run build
Output Directory: build/client
Install Command: npm install
Node Version: 20.x
```

### 2.2 Configure Environment Variables

In Vercel Dashboard → Settings → Environment Variables, add:

```env
VITE_AUTH0_DOMAIN=demo
VITE_AUTH0_CLIENT_ID=demo_client_id
VITE_AUTH0_AUDIENCE=https://api.financial-dashboard.com
VITE_API_URL=https://YOUR_BACKEND_URL.vercel.app/api/v1
```

**Important**: You'll update `VITE_API_URL` after deploying the backend in Step 3.

### 2.3 Deploy

1. Click "Deploy"
2. Wait for build to complete (~2-3 minutes)
3. Note your frontend URL: `https://your-project.vercel.app`

---

## ⚡ Step 3: Deploy Backend to Vercel

### 3.1 Create Backend Project

1. Go to https://vercel.com/new (new project)
2. Click "Import Project"
3. Select **same GitHub repository**
4. Configure project:

**Project Settings:**
```
Framework Preset: Other
Root Directory: backend
Build Command: pip install -r requirements.txt
Output Directory: (leave empty)
Install Command: (leave empty)
Node Version: 20.x
Python Version: 3.11
```

### 3.2 Create requirements.txt

Create `backend/requirements.txt`:
```bash
cd backend
cat > requirements.txt << 'EOF'
fastapi==0.115.12
uvicorn[standard]==0.34.0
python-jose[cryptography]==3.3.0
httpx==0.28.2
python-multipart==0.0.20
pydantic==2.10.6
pydantic-settings==2.7.1
EOF
```

Commit and push:
```bash
git add backend/requirements.txt
git commit -m "Add requirements.txt for Vercel"
git push
```

### 3.3 Configure Environment Variables

In Vercel Dashboard → Settings → Environment Variables:

```env
AUTH0_DOMAIN=demo
AUTH0_AUDIENCE=https://api.financial-dashboard.com
SECRET_KEY=demo_secret_key_not_used
BACKEND_CORS_ORIGINS=https://your-frontend.vercel.app,http://localhost:5173
PROJECT_NAME=Financial Dashboard API
API_V1_STR=/api/v1
ENVIRONMENT=production
DEBUG=False
```

### 3.4 Create vercel.json for Backend

Create `backend/vercel.json`:
```json
{
  "version": 2,
  "builds": [
    {
      "src": "src/main.py",
      "use": "@vercel/python"
    }
  ],
  "routes": [
    {
      "src": "/(.*)",
      "dest": "src/main.py"
    }
  ]
}
```

Commit and push:
```bash
git add backend/vercel.json
git commit -m "Add Vercel config for backend"
git push
```

### 3.5 Deploy

1. Click "Deploy" in Vercel
2. Wait for deployment (~3-5 minutes)
3. Note your backend URL: `https://your-backend.vercel.app`

---

## 🔗 Step 4: Connect Frontend to Backend

1. Go to Frontend Vercel project
2. Settings → Environment Variables
3. **Update** `VITE_API_URL`:
```env
VITE_API_URL=https://your-backend.vercel.app/api/v1
```

4. Redeploy frontend:
   - Go to Deployments tab
   - Click "..." on latest deployment
   - Click "Redeploy"

---

## ✅ Step 5: Verify Deployment

### Test Backend

Visit: `https://your-backend.vercel.app/docs`

Should show:
- Swagger UI with API documentation
- `/api/v1/portfolio/dashboard/stats` endpoint
- `/api/v1/portfolio/transactions` endpoint

Test endpoint:
```bash
curl https://your-backend.vercel.app/api/v1/health
```

Should return:
```json
{"status": "healthy"}
```

### Test Frontend

Visit: `https://your-frontend.vercel.app`

Should:
1. ✅ Redirect directly to `/dashboard/portfolio` (no login)
2. ✅ Show demo data in dashboard
3. ✅ Display portfolio stats
4. ✅ Show holdings table
5. ✅ Show snapshot history

### Test API Integration

Open browser DevTools → Network tab:
- Visit dashboard
- Should see API calls to `your-backend.vercel.app`
- Should return 200 status codes
- Should show demo data in responses

---

## 🔍 Troubleshooting

### Issue: Frontend shows blank page

**Solution**:
1. Check browser console for errors
2. Verify `VITE_API_URL` is correct in Vercel env vars
3. Redeploy frontend after changing env vars

### Issue: API returns 404 or 500

**Solution**:
1. Check backend logs in Vercel Dashboard
2. Verify `backend/vercel.json` exists
3. Verify `requirements.txt` has all dependencies
4. Check `AUTH0_DOMAIN=demo` is set

### Issue: CORS errors

**Solution**:
1. Add frontend URL to `BACKEND_CORS_ORIGINS`
2. Format: `https://your-frontend.vercel.app,http://localhost:5173`
3. Redeploy backend

### Issue: "Module not found" in backend

**Solution**:
1. Add missing package to `requirements.txt`
2. Commit and redeploy

### Issue: Data doesn't persist

**Expected behavior** - Demo mode uses in-memory storage:
- Data resets on each deployment
- Data resets when Vercel scales down functions
- This is intentional for demo purposes

---

## 📊 Demo Data

Demo mode automatically includes:
- 1 demo user
- 1 portfolio with 4 positions (AAPL, MSFT, GOOGL, CETES)
- 3 monthly snapshots (Oct, Nov, Dec 2024)
- Total portfolio value: $200,000 MXN

Data is loaded from `backend/src/core/demo_storage.py`.

---

## 🔄 Updating Deployment

### Update Frontend:
```bash
# Make changes to frontend code
git add frontend/
git commit -m "Update frontend"
git push
# Vercel auto-deploys on push
```

### Update Backend:
```bash
# Make changes to backend code
git add backend/
git commit -m "Update backend"
git push
# Vercel auto-deploys on push
```

### Manual Redeploy:
1. Go to Vercel Dashboard
2. Select project
3. Deployments → Click "..." → Redeploy

---

## 🎭 Demo Mode Features

✅ **Enabled**:
- View dashboard without login
- See demo portfolio data
- Explore all UI features
- API endpoints return demo data

❌ **Disabled**:
- File uploads (no database)
- Data persistence (in-memory only)
- Authentication
- Multi-user support

---

## 🔒 Security Notes

**Demo Mode is NOT SECURE:**
- No authentication
- No data isolation
- Public access to all data
- In-memory storage only

**Do NOT use Demo Mode with:**
- Real user data
- Production environments
- Sensitive information

---

## 📝 Vercel Configuration Files

### Root: vercel.json
```json
{
  "buildCommand": "cd frontend && npm install && npm run build",
  "outputDirectory": "frontend/build/client",
  "devCommand": "cd frontend && npm run dev",
  "installCommand": "cd frontend && npm install"
}
```

### Backend: backend/vercel.json
```json
{
  "version": 2,
  "builds": [
    {
      "src": "src/main.py",
      "use": "@vercel/python"
    }
  ],
  "routes": [
    {
      "src": "/(.*)",
      "dest": "src/main.py"
    }
  ]
}
```

### Backend: requirements.txt
```
fastapi==0.115.12
uvicorn[standard]==0.34.0
python-jose[cryptography]==3.3.0
httpx==0.28.2
python-multipart==0.0.20
pydantic==2.10.6
pydantic-settings==2.7.1
```

---

## ✅ Deployment Checklist

- [ ] Repository pushed to GitHub
- [ ] Frontend Vercel project created
- [ ] Frontend environment variables set
- [ ] Frontend deployed successfully
- [ ] Backend Vercel project created
- [ ] `requirements.txt` created
- [ ] `backend/vercel.json` created
- [ ] Backend environment variables set
- [ ] Backend deployed successfully
- [ ] Frontend `VITE_API_URL` updated with backend URL
- [ ] Frontend redeployed
- [ ] Tested: Frontend loads without login
- [ ] Tested: Dashboard shows demo data
- [ ] Tested: API endpoints return data
- [ ] No CORS errors in browser console

---

**Demo deployment ready! 🎉**

Share your demo: `https://your-frontend.vercel.app`
