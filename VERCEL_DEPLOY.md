# 🚀 Vercel Deployment Guide - Demo Mode

Guía para hacer deployment de Financial Dashboard en Vercel (cuenta gratuita).

---

## 📋 Prerequisitos

- Cuenta gratuita de Vercel (https://vercel.com/signup)
- Cuenta de GitHub
- Proyecto subido a GitHub

---

## 🔧 Paso 1: Preparar la rama de deployment

```fish
# Crear nueva rama desde main
git checkout -b demo-deployment

# Verificar que estás en la rama correcta
git branch

# Confirmar y subir cambios
git add .
git commit -m "Configure demo mode for Vercel deployment"
git push -u origin demo-deployment
```

---

## 🎨 Paso 2: Deploy del Frontend

### 2.1 Crear proyecto en Vercel

1. Ir a https://vercel.com/new
2. Click en "Import Project"
3. Seleccionar tu repositorio de GitHub
4. Seleccionar la rama `demo-deployment`
5. **En "Configure Project"**:
   - Framework Preset: **Vite**
   - Root Directory: **frontend** (muy importante)
   - Dejar todo lo demás por defecto (Vercel detecta automáticamente los comandos)

6. **ANTES de hacer Deploy**, ir a "Environment Variables" en la misma página y agregar:

```env
VITE_AUTH0_DOMAIN=demo
VITE_AUTH0_CLIENT_ID=demo_client_id
VITE_AUTH0_AUDIENCE=https://api.financial-dashboard.com
VITE_API_URL=TEMPORAL
```

**Nota**: `VITE_API_URL` se actualizará después del deploy del backend.

### 2.2 Deploy

1. Click "Deploy"
2. Esperar ~2-3 minutos
3. **Guardar la URL del frontend**: `https://tu-proyecto.vercel.app`

---

## ⚡ Paso 3: Deploy del Backend

### 3.1 Preparar archivos para Vercel

```fish
cd backend

# Renombrar pyproject.toml para evitar conflictos (Vercel usa requirements.txt)
mv pyproject.toml pyproject.toml.bak

# Crear requirements.txt con las dependencias necesarias
cat > requirements.txt << 'EOF'
fastapi==0.115.0
uvicorn[standard]==0.30.0
python-jose[cryptography]==3.3.0
httpx==0.27.0
python-multipart==0.0.9
pydantic==2.8.0
pydantic-settings==2.3.0
passlib[bcrypt]==1.7.4
sqlalchemy==2.0.23
alembic==1.13.0
EOF
```

### 3.2 Crear vercel.json para backend

```fish
cat > vercel.json << 'EOF'
{
  "version": 2,
  "builds": [
    {
      "src": "src/main.py",
      "use": "@vercel/python",
      "config": {
        "maxLambdaSize": "15mb"
      }
    }
  ],
  "routes": [
    {
      "src": "/(.*)",
      "dest": "src/main.py"
    }
  ],
  "env": {
    "PYTHONPATH": "/var/task"
  }
}
EOF
```

### 3.3 Subir archivos

```fish
# Volver al directorio raíz
cd ..

# Agregar archivos modificados
git add backend/requirements.txt backend/vercel.json backend/pyproject.toml.bak

# Si pyproject.toml original todavía existe, eliminarlo del git
git rm --cached backend/pyproject.toml 2>/dev/null || true

# Commit y push
git commit -m "Add Vercel config for backend"
git push origin demo-deployment
```

### 3.4 Crear proyecto backend en Vercel

1. Ir a https://vercel.com/new (nuevo proyecto)
2. Click en "Import Project"
3. Seleccionar el **mismo repositorio** de GitHub
4. Seleccionar la rama `demo-deployment`
5. **En "Configure Project"**:
   - Framework Preset: **Other**
   - Root Directory: **backend** (muy importante)
   - Dejar todo lo demás por defecto

6. **ANTES de hacer Deploy**, ir a "Environment Variables" en la misma página y agregar:

```env
AUTH0_DOMAIN=demo
AUTH0_AUDIENCE=https://api.financial-dashboard.com
SECRET_KEY=demo_secret_key_not_used
BACKEND_CORS_ORIGINS=https://tu-frontend.vercel.app,http://localhost:5173
PROJECT_NAME=Financial Dashboard API
API_V1_STR=/api/v1
ENVIRONMENT=production
```

**Importante**: Reemplazar `https://tu-frontend.vercel.app` con la URL del Paso 2.3.

### 3.5 Deploy

1. Click "Deploy"
2. Esperar ~3-5 minutos
3. **Guardar la URL del backend**: `https://tu-backend.vercel.app`

---

## 🔗 Paso 4: Conectar Frontend con Backend

1. Ir al proyecto Frontend en Vercel Dashboard
2. Settings → Environment Variables
3. Editar `VITE_API_URL`:
```env
VITE_API_URL=https://tu-backend.vercel.app/api/v1
```
4. Hacer redeploy:
   - Ir a pestaña "Deployments"
   - Click en "..." del último deployment
   - Click "Redeploy"

---

## ✅ Verificar Deployment

### Paso 1: Probar que el Backend está funcionando

**Opción A - Desde el navegador:**

1. Abrir en el navegador: `https://tu-backend.vercel.app/docs`
   - ✅ Debe mostrar Swagger UI (interfaz de documentación de FastAPI)
   - ✅ Debe listar todos los endpoints disponibles

2. Probar el endpoint de salud:
   - En Swagger UI, buscar el endpoint `/api/v1/health`
   - Click en "Try it out" → "Execute"
   - Debe retornar: `{"status": "healthy"}`

3. Probar el endpoint de demo portfolio:
   - Buscar el endpoint `/api/v1/portfolio/dashboard/stats`
   - Click en "Try it out" → "Execute"
   - ✅ Debe retornar datos del portfolio demo (sin pedir autenticación)

**Opción B - Desde la terminal:**

```fish
# Probar endpoint de salud
curl https://tu-backend.vercel.app/api/v1/health

# Debe retornar:
# {"status":"healthy"}

# Probar endpoint de stats (demo mode)
curl https://tu-backend.vercel.app/api/v1/portfolio/dashboard/stats

# Debe retornar JSON con datos del portfolio demo
```

**Verificar que Demo Mode está activo:**

En los logs de Vercel (pestaña "Logs" del deployment), debes ver:
```
🎭 DEMO MODE ENABLED - Using in-memory storage (no database)
```

### Paso 2: Probar el Frontend

**Visitar:** `https://tu-frontend.vercel.app`

Debe:
- ✅ Redirigir automáticamente a `/dashboard/portfolio` (sin login)
- ✅ Mostrar el dashboard con datos demo
- ✅ Mostrar estadísticas: Total Value, Cash, Invested
- ✅ Mostrar tabla de holdings con 4 posiciones (AAPL, MSFT, GOOGL, CETES)
- ✅ Mostrar gráfico de snapshot history

**Verificar en DevTools (F12):**

1. Abrir DevTools → Pestaña "Network"
2. Recargar la página
3. Filtrar por "Fetch/XHR"
4. Verificar:
   - ✅ Llamadas a `tu-backend.vercel.app/api/v1/portfolio/dashboard/stats`
   - ✅ Llamadas a `tu-backend.vercel.app/api/v1/portfolio/transactions`
   - ✅ Status Code: 200 OK
   - ✅ Response contiene datos JSON del portfolio

**Verificar en Console (F12):**
- ❌ No debe haber errores de CORS
- ❌ No debe haber errores de autenticación
- ✅ Puede haber un mensaje de "Demo Mode" (opcional)

### Paso 3: Verificar Integración Completa

**Test de datos en vivo:**

1. Abrir el frontend en el navegador
2. Verificar que los datos coincidan con los del backend:
   - Abrir DevTools → Network → Ver respuesta de `/dashboard/stats`
   - Los números deben coincidir con lo que se muestra en la UI

**Ejemplo de datos demo esperados:**
```json
{
  "netWorth": {"value": 200000, "label": "Total Value"},
  "cash": {"value": 50000, "label": "Cash"},
  "investments": {"value": 150000, "label": "Invested"},
  "performance": {
    "dailyChange": 5000,
    "dailyChangePercentage": 2.56,
    "trend": "up"
  }
}
```

### Troubleshooting Rápido

**Si el backend no carga:**
```fish
# Ver logs del deployment en Vercel
# O probar directamente el endpoint raíz
curl https://tu-backend.vercel.app/

# Debe retornar:
# {"message":"Welcome to Financial Dashboard API. Go to /docs for Swagger UI"}
```

**Si frontend muestra error 404 al llamar al backend:**
- Verificar que `VITE_API_URL` en las variables de entorno tenga la URL correcta
- Debe terminar en `/api/v1` (sin slash final)
- Ejemplo: `https://tu-backend.vercel.app/api/v1`

---

## 🔄 Actualizar Deployment

Vercel hace auto-deploy cuando haces push a la rama `demo-deployment`:

```fish
# Asegurarte de estar en la rama correcta
git checkout demo-deployment

# Hacer cambios y subir
git add .
git commit -m "Update changes"
git push origin demo-deployment
```

Vercel detectará el push y hará redeploy automáticamente.

---

## 🔍 Troubleshooting

### Frontend muestra página en blanco

1. Revisar consola del navegador (F12)
2. Verificar que `VITE_API_URL` esté correcto en Vercel
3. Hacer redeploy del frontend

### API retorna 404 o 500

1. Revisar logs en Vercel Dashboard
2. Verificar que `backend/vercel.json` exista
3. Verificar que `requirements.txt` esté completo
4. Verificar que `AUTH0_DOMAIN=demo` esté configurado

### Errores de CORS

1. Agregar URL del frontend a `BACKEND_CORS_ORIGINS`
2. Formato: `https://tu-frontend.vercel.app,http://localhost:5173`
3. Hacer redeploy del backend

---

## 📊 Datos Demo

El demo incluye automáticamente:
- 1 usuario demo
- 1 portfolio con 4 posiciones (AAPL, MSFT, GOOGL, CETES)
- 3 snapshots mensuales (Oct, Nov, Dic 2024)
- Valor total: $200,000 MXN

**Nota**: Los datos se resetean en cada deployment (almacenamiento en memoria).

---

## ✅ Checklist de Deployment

- [ ] Repositorio subido a GitHub
- [ ] Rama `demo-deployment` creada
- [ ] Frontend deployado en Vercel
- [ ] Variables de entorno del frontend configuradas
- [ ] `requirements.txt` creado
- [ ] `backend/vercel.json` creado
- [ ] Backend deployado en Vercel
- [ ] Variables de entorno del backend configuradas
- [ ] `VITE_API_URL` actualizado con URL del backend
- [ ] Frontend redesplegado
- [ ] Verificado: Frontend carga sin login
- [ ] Verificado: Dashboard muestra datos demo
- [ ] Verificado: API responde correctamente

---

**¡Demo listo! 🎉**

Comparte tu demo: `https://tu-frontend.vercel.app`
