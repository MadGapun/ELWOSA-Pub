# ELWOSA Deployment-Anleitung

## Voraussetzungen

- Docker 20.10+ und Docker Compose 2.0+
- PostgreSQL 14+
- Redis 6+
- 4GB RAM minimum (8GB empfohlen)
- 20GB freier Speicherplatz

## Schnellstart (Entwicklung)

```bash
# Repository klonen
git clone https://github.com/MadGapun/ELWOSA-Pub.git
cd ELWOSA-Pub

# Umgebungs-Template kopieren
cp .env.example .env

# .env mit Ihren Konfigurationen bearbeiten
# Wichtige Variablen:
# - DATABASE_URL
# - REDIS_URL
# - OPENAI_API_KEY (für KI-Features)
# - JWT_SECRET (sicheren Zufallsstring generieren)

# Alle Services starten
docker-compose up -d

# Service-Status prüfen
docker-compose ps

# Logs anzeigen
docker-compose logs -f

# Dashboard öffnen
open http://localhost:3000
```

## Produktions-Deployment

### 1. Datenbank-Setup

```sql
-- Produktionsdatenbank erstellen
CREATE DATABASE elwosa_production;
CREATE USER elwosa_user WITH ENCRYPTED PASSWORD 'sicheres_passwort';
GRANT ALL PRIVILEGES ON DATABASE elwosa_production TO elwosa_user;

-- Benötigte Extensions aktivieren
\c elwosa_production
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pg_trgm";
```

### 2. Umgebungskonfiguration

Produktions-`.env.production` erstellen:

```bash
# Datenbank
DATABASE_URL=postgresql://elwosa_user:sicheres_passwort@db-host:5432/elwosa_production
DATABASE_POOL_SIZE=20

# Redis
REDIS_URL=redis://redis-host:6379/0

# API Keys
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-ant-...

# Sicherheit
JWT_SECRET=generiert-mit-openssl-rand-base64-32
JWT_EXPIRY=15m
REFRESH_TOKEN_EXPIRY=7d

# Service URLs
TASK_SERVICE_URL=http://task-service:8001
AUTH_SERVICE_URL=http://auth-service:8003
MEMORY_SERVICE_URL=http://memory-service:8765
AI_BRIDGE_URL=http://ai-bridge:8006

# Frontend
REACT_APP_API_URL=https://api.ihre-domain.com
REACT_APP_WS_URL=wss://ws.ihre-domain.com
```

### 3. Docker Produktions-Build

```dockerfile
# Multi-Stage Build für optimierte Images
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
  jwt-secret: "ihr-secret-hier"
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

### 5. Datenbank-Migrationen

```bash
# Migrationen ausführen
docker-compose run --rm task-service alembic upgrade head

# Initialen Admin-Benutzer erstellen
docker-compose run --rm auth-service python scripts/create_admin.py
```

## Monitoring-Setup

### Prometheus-Konfiguration

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

### Grafana-Dashboards

Bereitgestellte Dashboards aus `monitoring/grafana-dashboards/` importieren:
- Service Health Dashboard
- Task Processing Metriken
- KI-Model Performance
- Datenbank-Performance

## Sicherheits-Härtung

### 1. Netzwerk-Sicherheit

```nginx
# nginx.conf
server {
    listen 443 ssl http2;
    server_name api.ihre-domain.com;

    ssl_certificate /etc/nginx/ssl/cert.pem;
    ssl_certificate_key /etc/nginx/ssl/key.pem;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;

    # Sicherheits-Header
    add_header Strict-Transport-Security "max-age=31536000" always;
    add_header X-Frame-Options "DENY" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;

    # Rate Limiting
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

### 2. Datenbank-Sicherheit

```sql
-- SSL für Datenbankverbindungen aktivieren
ALTER SYSTEM SET ssl = on;
ALTER SYSTEM SET ssl_cert_file = '/var/lib/postgresql/server.crt';
ALTER SYSTEM SET ssl_key_file = '/var/lib/postgresql/server.key';

-- Row Level Security für Multi-Tenancy
ALTER TABLE tasks ENABLE ROW LEVEL SECURITY;

CREATE POLICY tenant_isolation ON tasks
  FOR ALL
  USING (tenant_id = current_setting('app.current_tenant')::int);
```

## Backup & Recovery

### Automatisierte Backups

```bash
#!/bin/bash
# backup.sh
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="/backups"

# Datenbank-Backup
pg_dump $DATABASE_URL > $BACKUP_DIR/elwosa_$DATE.sql

# Komprimieren und verschlüsseln
tar -czf - $BACKUP_DIR/elwosa_$DATE.sql | \
  openssl enc -aes-256-cbc -salt -out $BACKUP_DIR/elwosa_$DATE.tar.gz.enc

# Upload zu S3
aws s3 cp $BACKUP_DIR/elwosa_$DATE.tar.gz.enc s3://elwosa-backups/

# Alte Backups löschen (30 Tage behalten)
find $BACKUP_DIR -name "*.sql" -mtime +30 -delete
```

### Recovery-Verfahren

```bash
# Aus Backup wiederherstellen
openssl enc -d -aes-256-cbc -in elwosa_backup.tar.gz.enc | tar -xzf -
psql $DATABASE_URL < elwosa_backup.sql

# Datenintegrität prüfen
docker-compose run --rm task-service python scripts/verify_data.py
```

## Performance-Optimierung

### PostgreSQL-Optimierung

```sql
-- postgresql.conf Anpassungen
shared_buffers = 25% des RAMs
effective_cache_size = 75% des RAMs
maintenance_work_mem = 256MB
work_mem = 4MB
max_connections = 200

-- Optimierte Indizes erstellen
CREATE INDEX CONCURRENTLY idx_tasks_created_at ON tasks(created_at DESC);
CREATE INDEX CONCURRENTLY idx_tasks_assignee_status ON tasks(assigned_to, status);
CREATE INDEX CONCURRENTLY idx_tasks_metadata_gin ON tasks USING gin(metadata);
```

### Redis-Konfiguration

```conf
# redis.conf
maxmemory 2gb
maxmemory-policy allkeys-lru
save 900 1
save 300 10
save 60 10000
```

## Troubleshooting

### Häufige Probleme

1. **Service startet nicht**
   ```bash
   # Logs prüfen
   docker-compose logs -f service-name
   
   # Umgebungsvariablen verifizieren
   docker-compose config
   ```

2. **Datenbankverbindungsfehler**
   ```bash
   # Verbindung testen
   docker-compose run --rm task-service python -c "
   from sqlalchemy import create_engine
   engine = create_engine('$DATABASE_URL')
   engine.connect()
   print('Verbindung erfolgreich')
   "
   ```

3. **KI-Service Timeouts**
   ```python
   # Timeout in Konfiguration erhöhen
   AI_REQUEST_TIMEOUT = 30  # Sekunden
   AI_MAX_RETRIES = 3
   ```

### Health Checks

```bash
# Alle Services prüfen
curl http://localhost:8001/health  # Task Service
curl http://localhost:8003/health  # Auth Service
curl http://localhost:8765/health  # Memory Service
curl http://localhost:8006/health  # AI Bridge
```

## Skalierungs-Richtlinien

### Horizontale Skalierung

- **Task Service**: Skalierung basierend auf CPU-Nutzung (Ziel 70%)
- **Auth Service**: Meist 2-3 Instanzen ausreichend
- **Memory Service**: Einzelne Instanz mit Redis-Clustering
- **AI Bridge**: Skalierung basierend auf Request-Queue-Länge

### Vertikale Skalierung

Empfohlene Spezifikationen nach Last:

| Last | Task Service | Auth Service | Memory Service | Datenbank |
|------|-------------|--------------|----------------|----------|
| Klein (< 100 Benutzer) | 2 CPU, 4GB RAM | 1 CPU, 2GB RAM | 1 CPU, 2GB RAM | 2 CPU, 8GB RAM |
| Mittel (100-1000 Benutzer) | 4 CPU, 8GB RAM | 2 CPU, 4GB RAM | 2 CPU, 4GB RAM | 4 CPU, 16GB RAM |
| Groß (1000+ Benutzer) | 8 CPU, 16GB RAM | 4 CPU, 8GB RAM | 4 CPU, 8GB RAM | 8 CPU, 32GB RAM |

---

Diese Deployment-Anleitung bietet einen umfassenden Weg von der Entwicklung bis zum Produktions-Deployment und gewährleistet Zuverlässigkeit, Sicherheit und Skalierbarkeit für ELWOSA-Installationen.