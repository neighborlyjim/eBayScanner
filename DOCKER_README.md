# eBay Scanner Docker Setup

This Docker Compose setup provides a complete environment for the eBay Scanner application with PostgreSQL database, Redis caching, and separate containers for the web application and background worker.

## 🏗️ Architecture

- **web**: Flask web application (port 5000)
- **worker**: Background tasks and scheduled scanning
- **db**: PostgreSQL database (port 5432)
- **redis**: Redis cache (port 6379)

## 🚀 Quick Start

### Prerequisites
- Docker and Docker Compose installed
- Your eBay API keys in `.env` file

### 1. Prepare Environment
```bash
# Copy your API keys to .env file
cp .env.example .env
# Edit .env with your actual eBay API keys
```

### 2. Development Mode (with hot reload)
```bash
# Start all services in development mode
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

### 3. Production Mode
```bash
# Start in production mode
docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d

# View logs
docker-compose logs -f web
```

## 📋 Available Commands

### Container Management
```bash
# Start services
docker-compose up -d

# Stop services
docker-compose down

# Restart a specific service
docker-compose restart web

# View service status
docker-compose ps

# View logs
docker-compose logs -f [service_name]
```

### Database Operations
```bash
# Run database migrations
docker-compose exec web alembic upgrade head

# Create new migration
docker-compose exec web alembic revision --autogenerate -m "description"

# Access PostgreSQL shell
docker-compose exec db psql -U ebay_user -d ebay_scanner

# Backup database
docker-compose exec db pg_dump -U ebay_user ebay_scanner > backup.sql

# Restore database
docker-compose exec -T db psql -U ebay_user ebay_scanner < backup.sql
```

### Application Operations
```bash
# Run scanner manually
docker-compose exec worker python scout.py

# Test API connection
docker-compose exec web python test_connection.py

# Access Python shell
docker-compose exec web python

# Access container shell
docker-compose exec web bash
```

## 🔧 Configuration

### Environment Variables
The following environment variables are configured in `docker-compose.yml`:

**Database:**
- `DB_HOST=db`
- `DB_NAME=ebay_scanner`
- `DB_USER=ebay_user`
- `DB_PASSWORD=ebay_password`

**eBay API (from .env file):**
- `EBAY_CLIENT_ID`
- `EBAY_CLIENT_SECRET`
- `EBAY_APP_ID`
- `EBAY_DEV_ID`

### Ports
- **5000**: Web application
- **5432**: PostgreSQL database
- **6379**: Redis cache

### Volumes
- `postgres_data`: Persistent database storage
- `redis_data`: Persistent Redis storage
- `./logs`: Application logs

## 🔍 Monitoring & Debugging

### Health Checks
```bash
# Check service health
docker-compose ps

# Check database health
docker-compose exec db pg_isready -U ebay_user -d ebay_scanner

# Check web application health
curl http://localhost:5000/health
```

### Logs
```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f web
docker-compose logs -f worker
docker-compose logs -f db

# Last 100 lines
docker-compose logs --tail=100 web
```

### Resource Usage
```bash
# View resource usage
docker stats

# View container details
docker-compose exec web ps aux
```

## 🛠️ Development

### Code Changes
In development mode (`docker-compose.override.yml`), your local code is mounted into the container, so changes are reflected immediately.

### Adding Dependencies
1. Add package to `requirements.txt`
2. Rebuild container: `docker-compose build web`
3. Restart services: `docker-compose up -d`

### Database Schema Changes
1. Make model changes in your code
2. Create migration: `docker-compose exec web alembic revision --autogenerate -m "description"`
3. Apply migration: `docker-compose exec web alembic upgrade head`

## 🚨 Troubleshooting

### Common Issues

**Database connection errors:**
```bash
# Check database is running
docker-compose ps db

# Check database logs
docker-compose logs db

# Restart database
docker-compose restart db
```

**Web application won't start:**
```bash
# Check application logs
docker-compose logs web

# Check if dependencies are installed
docker-compose exec web pip list

# Rebuild container
docker-compose build --no-cache web
```

**Port conflicts:**
```bash
# Check what's using the port
netstat -tulpn | grep :5000

# Use different ports in docker-compose.yml
ports:
  - "5001:5000"  # Use port 5001 instead
```

## 🔒 Security Notes

- Database credentials are configured in `docker-compose.yml`
- eBay API keys are loaded from `.env` file
- The `.env` file is in `.gitignore` to prevent committing secrets
- Application runs as non-root user in container
- Use `docker-compose.prod.yml` for production deployments

## 📊 Scaling

For high-traffic scenarios:
```bash
# Scale worker containers
docker-compose up -d --scale worker=3

# Scale web containers (requires load balancer)
docker-compose up -d --scale web=2
```
