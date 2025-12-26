#!/bin/bash

echo "🚀 Financial Dashboard - Starting from Zero"
echo "==========================================="
echo ""

# Colores para el output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Función para imprimir con color
print_step() {
    echo -e "${BLUE}▶ $1${NC}"
}

print_success() {
    echo -e "${GREEN}✓ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠ $1${NC}"
}

print_error() {
    echo -e "${RED}✗ $1${NC}"
}

# 1. Detener y limpiar contenedores existentes
print_step "Step 1: Cleaning up existing containers..."
docker-compose down -v
print_success "Containers stopped and volumes removed"
echo ""

# 2. Reconstruir las imágenes (sin caché para asegurar build limpio)
print_step "Step 2: Building Docker images (this may take a few minutes)..."
docker-compose build --no-cache
if [ $? -eq 0 ]; then
    print_success "Docker images built successfully"
else
    print_error "Failed to build Docker images"
    exit 1
fi
echo ""

# 3. Iniciar la base de datos primero
print_step "Step 3: Starting PostgreSQL database..."
docker-compose up -d db
sleep 5  # Esperar a que PostgreSQL esté listo
print_success "Database is running"
echo ""

# 4. Verificar que la base de datos esté lista
print_step "Step 4: Waiting for database to be ready..."
until docker-compose exec -T db pg_isready -U postgres > /dev/null 2>&1; do
    echo "Waiting for database connection..."
    sleep 2
done
print_success "Database is ready to accept connections"
echo ""

# 5. Ejecutar migraciones de Alembic
print_step "Step 5: Running database migrations..."
docker-compose run --rm backend poetry run alembic upgrade head
if [ $? -eq 0 ]; then
    print_success "Database migrations completed successfully"
else
    print_error "Failed to run migrations"
    exit 1
fi
echo ""

# 6. Verificar las tablas creadas
print_step "Step 6: Verifying database schema..."
docker-compose exec -T db psql -U postgres -d financial_db -c "\dt" | grep -E "users|portfolios|positions"
if [ $? -eq 0 ]; then
    print_success "Database tables verified (users, portfolios, positions)"
else
    print_warning "Could not verify tables, but continuing..."
fi
echo ""

# 7. Iniciar el backend
print_step "Step 7: Starting FastAPI backend..."
docker-compose up -d backend
sleep 3
print_success "Backend is starting..."
echo ""

# 8. Verificar que el backend esté saludable
print_step "Step 8: Checking backend health..."
MAX_RETRIES=10
RETRY_COUNT=0
until curl -s http://localhost:8000/api/v1/health > /dev/null 2>&1; do
    RETRY_COUNT=$((RETRY_COUNT+1))
    if [ $RETRY_COUNT -ge $MAX_RETRIES ]; then
        print_error "Backend failed to start after $MAX_RETRIES attempts"
        print_warning "Check logs with: docker-compose logs backend"
        exit 1
    fi
    echo "Waiting for backend to be healthy... (attempt $RETRY_COUNT/$MAX_RETRIES)"
    sleep 3
done
print_success "Backend is healthy and responding"
echo ""

# 9. Iniciar el frontend
print_step "Step 9: Starting React frontend..."
docker-compose up -d frontend
sleep 5
print_success "Frontend is starting..."
echo ""

# 10. Mostrar logs en tiempo real (opcional)
echo ""
echo "==========================================="
print_success "All services are running!"
echo "==========================================="
echo ""
echo "📊 Service URLs:"
echo "   - Frontend:  http://localhost:5173"
echo "   - Backend:   http://localhost:8000"
echo "   - API Docs:  http://localhost:8000/docs"
echo "   - Health:    http://localhost:8000/api/v1/health"
echo ""
echo "🗄️  Database:"
echo "   - Host: localhost:5432"
echo "   - Database: financial_db"
echo "   - User: postgres"
echo "   - Password: postgres"
echo ""
echo "📝 Useful commands:"
echo "   - View logs:           docker-compose logs -f"
echo "   - View backend logs:   docker-compose logs -f backend"
echo "   - View frontend logs:  docker-compose logs -f frontend"
echo "   - Stop all:            docker-compose down"
echo "   - Restart all:         docker-compose restart"
echo "   - Access database:     docker-compose exec db psql -U postgres -d financial_db"
echo ""
print_warning "Press Ctrl+C to stop viewing logs (services will keep running)"
echo ""

# Seguir los logs de todos los servicios
docker-compose logs -f
