# ELWOSA Deployment Guide

This guide walks you through deploying ELWOSA in various environments.

## Prerequisites

- Docker 20.10+ and Docker Compose 2.0+
- PostgreSQL 14+ (or use the included Docker container)
- Python 3.9+ (for local development)
- Node.js 16+ (for frontend development)
- 4GB RAM minimum (8GB recommended)

## Quick Start with Docker

The fastest way to get ELWOSA running:

```bash
# Clone the repository
git clone https://github.com/MadGapun/ELWOSA-Pub.git
cd ELWOSA-Pub

# Copy environment template
cp .env.example .env

# Edit .env with your configuration
nano .env

# Start all services
docker-compose up -d

# Check service health
docker-compose ps
```

Services will be available at:
- Dashboard: http://localhost:3000
- Task API: http://localhost:8001
- Memory API: http://localhost:8765
- AI Bridge: http://localhost:8006
- Auth API: http://localhost:8003

## Manual Deployment

### 1. Database Setup

```sql
-- Create database
CREATE DATABASE elwosa_pm;

-- Create user
CREATE USER elwosa_user WITH PASSWORD 'secure_password';

-- Grant privileges
GRANT ALL PRIVILEGES ON DATABASE elwosa_pm TO elwosa_user;
```

Run migrations:
```bash
cd database
psql -U elwosa_user -d elwosa_pm -f migrations/001_initial_schema.sql
```

### 2. Backend Services

Each service can be deployed independently:

#### Task API
```bash
cd services/task-api
pip install -r requirements.txt
export DATABASE_URL="postgresql://elwosa_user:password@localhost/elwosa_pm"
uvicorn main:app --host 0.0.0.0 --port 8001
```

#### Memory Service
```bash
cd services/memory-service
pip install -r requirements.txt
export MEMORY_DB_PATH="./data/memories.db"
python memory_service.py
```

#### AI Bridge
```bash
cd services/ai-bridge
pip install -r requirements.txt
export OPENAI_API_KEY="your-key-here"
python ai_bridge.py
```

### 3. Frontend Dashboard

```bash
cd frontend
npm install
npm run build

# Serve with nginx
cp -r dist/* /var/www/html/
```

## Production Deployment

### Using Kubernetes

Deploy to Kubernetes cluster:

```bash
# Apply configurations
kubectl apply -f k8s/namespace.yaml
kubectl apply -f k8s/configmap.yaml
kubectl apply -f k8s/secrets.yaml

# Deploy services
kubectl apply -f k8s/postgres/
kubectl apply -f k8s/services/
kubectl apply -f k8s/frontend/

# Check deployment
kubectl get pods -n elwosa
```

### Using Docker Swarm

Initialize swarm and deploy:

```bash
# Initialize swarm
docker swarm init

# Deploy stack
docker stack deploy -c docker-compose.prod.yml elwosa

# Check services
docker service ls
```

## Configuration

### Environment Variables

Key environment variables for each service:

```bash
# Database
DATABASE_URL=postgresql://user:pass@host/db
DB_POOL_SIZE=20

# Task API
TASK_API_PORT=8001
TASK_API_WORKERS=4

# Memory Service
MEMORY_DB_PATH=/data/memories.db
MEMORY_SERVICE_PORT=8765

# AI Bridge
OPENAI_API_KEY=sk-...
OLLAMA_HOST=http://localhost:11434
AI_PROVIDER=openai

# Auth Service
JWT_SECRET=your-secret-key
JWT_EXPIRY=3600
```

### Nginx Configuration

Example nginx configuration for production:

```nginx
server {
    listen 80;
    server_name elwosa.example.com;

    # Frontend
    location / {
        root /var/www/elwosa;
        try_files $uri $uri/ /index.html;
    }

    # API Proxy
    location /api/tasks {
        proxy_pass http://localhost:8001;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    location /api/memory {
        proxy_pass http://localhost:8765;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

## SSL/TLS Setup

For production, always use HTTPS:

```bash
# Using Let's Encrypt
certbot --nginx -d elwosa.example.com
```

## Monitoring

### Health Checks

All services expose health endpoints:
- `GET /health` - Basic health check
- `GET /metrics` - Prometheus metrics

### Logging

Configure centralized logging:

```yaml
logging:
  driver: "json-file"
  options:
    max-size: "10m"
    max-file: "3"
```

## Backup & Recovery

### Database Backup

Automated daily backups:

```bash
# Backup script
#!/bin/bash
pg_dump -U elwosa_user elwosa_pm > backup_$(date +%Y%m%d).sql

# Restore
psql -U elwosa_user elwosa_pm < backup_20250623.sql
```

### Memory Service Backup

```bash
# Backup SQLite database
cp /data/memories.db /backup/memories_$(date +%Y%m%d).db
```

## Troubleshooting

### Common Issues

1. **Services not starting**: Check logs with `docker-compose logs service-name`
2. **Database connection errors**: Verify DATABASE_URL and network connectivity
3. **CORS issues**: Ensure CORS middleware is configured correctly
4. **Performance issues**: Check resource limits and scaling settings

### Debug Mode

Enable debug logging:

```bash
export LOG_LEVEL=DEBUG
export DEBUG=true
```

## Security Considerations

1. **Use strong passwords** for database and JWT secrets
2. **Enable firewall** rules for service ports
3. **Regular updates** of dependencies
4. **Network isolation** between services
5. **Regular backups** of data

## Support

For deployment support:
- Check our [FAQ](./FAQ.md)
- Join our [Discord community](https://discord.gg/elwosa)
- Open an [issue on GitHub](https://github.com/MadGapun/ELWOSA-Pub/issues)

---
*Last updated: June 2025*
