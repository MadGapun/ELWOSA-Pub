# ELWOSA Deployment Guide

## Prerequisites

- Docker 20.10+ and Docker Compose 2.0+
- PostgreSQL 14+
- Redis 6+
- 4GB RAM minimum (8GB recommended)
- 20GB free disk space

## Quick Start (Development)

```bash
# Clone the repository
git clone https://github.com/yourusername/ELWOSA.git
cd ELWOSA

# Copy environment template
cp .env.example .env

# Edit .env with your configurations
# Important variables:
# - DATABASE_URL
# - REDIS_URL
# - OPENAI_API_KEY (for AI features)
# - JWT_SECRET (generate a secure random string)

# Start all services
docker-compose up -d

# Check service health
docker-compose ps

# View logs
docker-compose logs -f

# Access the dashboard
open http://localhost:3000
```

## Production Deployment

### 1. Database Setup

```sql
-- Create production database
CREATE DATABASE elwosa_production;
CREATE USER elwosa_user WITH ENCRYPTED PASSWORD 'secure_password';
GRANT ALL PRIVILEGES ON DATABASE elwosa_production TO elwosa_user;

-- Enable required extensions
\c elwosa_production
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pg_trgm";
```

### 2. Environment Configuration

Create production `.env.production`:

```bash
# Database
DATABASE_URL=postgresql://elwosa_user:secure_password@db-host:5432/elwosa_production
DATABASE_POOL_SIZE=20

# Redis
REDIS_URL=redis://redis-host:6379/0

# API Keys
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-ant-...

# Security
JWT_SECRET=generate-using-openssl-rand-base64-32
JWT_EXPIRY=15m
REFRESH_TOKEN_EXPIRY=7d

# Service URLs
TASK_SERVICE_URL=http://task-service:8001
AUTH_SERVICE_URL=http://auth-service:8003
MEMORY_SERVICE_URL=http://memory-service:8765
AI_BRIDGE_URL=http://ai-bridge:8006

# Frontend
REACT_APP_API_URL=https://api.your-domain.com
REACT_APP_WS_URL=wss://ws.your-domain.com
```

### 3. Docker Production Build

```dockerfile
# Multi-stage build for optimized images
FROM node:18-alpine AS frontend-builder
WORKDIR /app
COPY frontend/package*.json ./
RUN npm ci --only=production
COPY frontend/ ./
RUN npm run build

FROM python:3.11-slim AS backend-builder
WORKDIR /app
COPY services/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

FROM python:3.11-slim
WORKDIR /app
COPY --from=backend-builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY services/ ./
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### 4. Kubernetes Deployment

```yaml
# namespace.yaml
apiVersion: v1
kind: Namespace
metadata:
  name: elwosa

---
# configmap.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: elwosa-config
  namespace: elwosa
data:
  TASK_SERVICE_URL: "http://task-service:8001"
  AUTH_SERVICE_URL: "http://auth-service:8003"
  MEMORY_SERVICE_URL: "http://memory-service:8765"

---
# secrets.yaml
apiVersion: v1
kind: Secret
metadata:
  name: elwosa-secrets
  namespace: elwosa
type: Opaque
stringData:
  database-url: "postgresql://user:pass@postgres:5432/elwosa"
  jwt-secret: "your-secret-here"
  openai-api-key: "sk-..."

---
# deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: task-service
  namespace: elwosa
spec:
  replicas: 3
  selector:
    matchLabels:
      app: task-service
  template:
    metadata:
      labels:
        app: task-service
    spec:
      containers:
      - name: task-service
        image: elwosa/task-service:latest
        ports:
        - containerPort: 8001
        env:
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: elwosa-secrets
              key: database-url
        envFrom:
        - configMapRef:
            name: elwosa-config
        resources:
          requests:
            memory: "256Mi"
            cpu: "250m"
          limits:
            memory: "512Mi"
            cpu: "500m"
```

### 5. Database Migrations

```bash
# Run migrations
docker-compose run --rm task-service alembic upgrade head

# Create initial admin user
docker-compose run --rm auth-service python scripts/create_admin.py
```

## Monitoring Setup

### Prometheus Configuration

```yaml
# prometheus.yml
global:
  scrape_interval: 15s

scrape_configs:
  - job_name: 'elwosa-services'
    static_configs:
      - targets:
        - task-service:8001
        - auth-service:8003
        - memory-service:8765
        - ai-bridge:8006
```

### Grafana Dashboards

Import provided dashboards from `monitoring/grafana-dashboards/`:
- Service Health Dashboard
- Task Processing Metrics
- AI Model Performance
- Database Performance

## Security Hardening

### 1. Network Security

```nginx
# nginx.conf
server {
    listen 443 ssl http2;
    server_name api.your-domain.com;

    ssl_certificate /etc/nginx/ssl/cert.pem;
    ssl_certificate_key /etc/nginx/ssl/key.pem;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;

    # Security headers
    add_header Strict-Transport-Security "max-age=31536000" always;
    add_header X-Frame-Options "DENY" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;

    # Rate limiting
    limit_req_zone $binary_remote_addr zone=api:10m rate=10r/s;
    limit_req zone=api burst=20 nodelay;

    location / {
        proxy_pass http://api-gateway;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header Host $host;
    }
}
```

### 2. Database Security

```sql
-- Enable SSL for database connections
ALTER SYSTEM SET ssl = on;
ALTER SYSTEM SET ssl_cert_file = '/var/lib/postgresql/server.crt';
ALTER SYSTEM SET ssl_key_file = '/var/lib/postgresql/server.key';

-- Row Level Security for multi-tenancy
ALTER TABLE tasks ENABLE ROW LEVEL SECURITY;

CREATE POLICY tenant_isolation ON tasks
  FOR ALL
  USING (tenant_id = current_setting('app.current_tenant')::int);
```

## Backup & Recovery

### Automated Backups

```bash
#!/bin/bash
# backup.sh
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="/backups"

# Database backup
pg_dump $DATABASE_URL > $BACKUP_DIR/elwosa_$DATE.sql

# Compress and encrypt
tar -czf - $BACKUP_DIR/elwosa_$DATE.sql | \
  openssl enc -aes-256-cbc -salt -out $BACKUP_DIR/elwosa_$DATE.tar.gz.enc

# Upload to S3
aws s3 cp $BACKUP_DIR/elwosa_$DATE.tar.gz.enc s3://elwosa-backups/

# Cleanup old backups (keep 30 days)
find $BACKUP_DIR -name "*.sql" -mtime +30 -delete
```

### Recovery Procedure

```bash
# Restore from backup
openssl enc -d -aes-256-cbc -in elwosa_backup.tar.gz.enc | tar -xzf -
psql $DATABASE_URL < elwosa_backup.sql

# Verify data integrity
docker-compose run --rm task-service python scripts/verify_data.py
```

## Performance Tuning

### PostgreSQL Optimization

```sql
-- postgresql.conf adjustments
shared_buffers = 25% of RAM
effective_cache_size = 75% of RAM
maintenance_work_mem = 256MB
work_mem = 4MB
max_connections = 200

-- Create optimized indexes
CREATE INDEX CONCURRENTLY idx_tasks_created_at ON tasks(created_at DESC);
CREATE INDEX CONCURRENTLY idx_tasks_assignee_status ON tasks(assigned_to, status);
CREATE INDEX CONCURRENTLY idx_tasks_metadata_gin ON tasks USING gin(metadata);
```

### Redis Configuration

```conf
# redis.conf
maxmemory 2gb
maxmemory-policy allkeys-lru
save 900 1
save 300 10
save 60 10000
```

## Troubleshooting

### Common Issues

1. **Service won't start**
   ```bash
   # Check logs
   docker-compose logs -f service-name
   
   # Verify environment variables
   docker-compose config
   ```

2. **Database connection errors**
   ```bash
   # Test connection
   docker-compose run --rm task-service python -c "
   from sqlalchemy import create_engine
   engine = create_engine('$DATABASE_URL')
   engine.connect()
   print('Connection successful')
   "
   ```

3. **AI Service timeouts**
   ```python
   # Increase timeout in config
   AI_REQUEST_TIMEOUT = 30  # seconds
   AI_MAX_RETRIES = 3
   ```

### Health Checks

```bash
# Check all services
curl http://localhost:8001/health  # Task Service
curl http://localhost:8003/health  # Auth Service
curl http://localhost:8765/health  # Memory Service
curl http://localhost:8006/health  # AI Bridge
```

## Scaling Guidelines

### Horizontal Scaling

- **Task Service**: Scale based on CPU usage (target 70%)
- **Auth Service**: Usually 2-3 instances sufficient
- **Memory Service**: Single instance with Redis clustering
- **AI Bridge**: Scale based on request queue length

### Vertical Scaling

Recommended specifications by load:

| Load | Task Service | Auth Service | Memory Service | Database |
|------|-------------|--------------|----------------|----------|
| Small (< 100 users) | 2 CPU, 4GB RAM | 1 CPU, 2GB RAM | 1 CPU, 2GB RAM | 2 CPU, 8GB RAM |
| Medium (100-1000 users) | 4 CPU, 8GB RAM | 2 CPU, 4GB RAM | 2 CPU, 4GB RAM | 4 CPU, 16GB RAM |
| Large (1000+ users) | 8 CPU, 16GB RAM | 4 CPU, 8GB RAM | 4 CPU, 8GB RAM | 8 CPU, 32GB RAM |

---

This deployment guide provides a comprehensive path from development to production deployment, ensuring reliability, security, and scalability for ELWOSA installations.