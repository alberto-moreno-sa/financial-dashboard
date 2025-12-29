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
fastapi==0.115.12
uvicorn[standard]==0.34.0
python-jose[cryptography]==3.3.0
httpx==0.28.2
python-multipart==0.0.20
pydantic==2.10.6
pydantic-settings==2.7.1
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

### Probar Backend

Visitar: `https://tu-backend.vercel.app/docs`

Debe mostrar Swagger UI con la documentación de la API.

Probar endpoint:
```fish
curl https://tu-backend.vercel.app/api/v1/health
```

Debe retornar:
```json
{"status": "healthy"}
```

### Probar Frontend

Visitar: `https://tu-frontend.vercel.app`

Debe:
- ✅ Redirigir directamente al dashboard (sin login)
- ✅ Mostrar datos demo del portfolio
- ✅ Mostrar estadísticas
- ✅ Mostrar tabla de holdings
- ✅ Mostrar historial de snapshots

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
