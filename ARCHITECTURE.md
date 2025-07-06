# ELWOSA System-Architektur

## Überblick

ELWOSA implementiert eine moderne Microservices-Architektur, die für Skalierbarkeit, Wartbarkeit und Erweiterbarkeit konzipiert ist. Das System folgt Domain-Driven Design (DDD) Prinzipien und implementiert verschiedene Enterprise-Patterns.

## System-Komponenten

```mermaid
graph TB
    subgraph "Frontend-Schicht"
        UI[React Dashboard]
        MW[Mobile Web App]
    end
    
    subgraph "API Gateway"
        GW[NGINX Reverse Proxy]
    end
    
    subgraph "Service-Schicht"
        TS[Task Service<br/>FastAPI:8001]
        AS[Auth Service<br/>FastAPI:8003]
        MS[Memory Service<br/>WebSocket:8765]
        AI[AI Bridge Service<br/>FastAPI:8006]
    end
    
    subgraph "Daten-Schicht"
        PG[(PostgreSQL<br/>Tasks & Users)]
        CACHE[(Redis Cache<br/>Sessions)]
        MEM[(Memory Store<br/>JSON)]
    end
    
    subgraph "Externe Services"
        GPT[OpenAI API]
        LLM[Lokale LLMs]
    end
    
    UI --> GW
    MW --> GW
    GW --> TS
    GW --> AS
    GW --> MS
    GW --> AI
    
    TS --> PG
    AS --> PG
    AS --> CACHE
    MS --> MEM
    AI --> GPT
    AI --> LLM
```

## Kern-Services

### Task Management Service
- **Technologie**: Python FastAPI
- **Port**: 8001
- **Verantwortlichkeiten**:
  - CRUD-Operationen für Tasks
  - Prioritäts-Management
  - Schritt-Verfolgung
  - Echtzeit-Updates

### Authentication Service
- **Technologie**: Python FastAPI
- **Port**: 8003
- **Features**:
  - JWT-Token-Generierung
  - Benutzer-Management
  - Rollenbasierte Zugriffskontrolle
  - Session-Management via Redis

### Memory Service
- **Technologie**: Python WebSocket Server
- **Port**: 8765
- **Zweck**: Persistenter System-Speicher für KI-Kontext
- **Features**:
  - Echtzeit-Speicher-Updates
  - Kontext-Bewahrung
  - WebSocket-Streaming

### AI Bridge Service
- **Technologie**: Python FastAPI
- **Port**: 8006
- **Fähigkeiten**:
  - Multi-Model-Support (GPT-4, Llama, etc.)
  - Streaming-Antworten
  - Kontext-Management
  - Load Balancing

## Datenfluss

```mermaid
sequenceDiagram
    participant U as Benutzer
    participant D as Dashboard
    participant G as Gateway
    participant T as Task Service
    participant A as Auth Service
    participant DB as PostgreSQL
    
    U->>D: Login-Anfrage
    D->>G: POST /auth/login
    G->>A: Authentifizierung
    A->>DB: Anmeldedaten prüfen
    DB-->>A: Benutzerdaten
    A-->>G: JWT Token
    G-->>D: Auth-Response
    D-->>U: Dashboard-Zugriff
    
    U->>D: Task erstellen
    D->>G: POST /tasks
    G->>A: Token prüfen
    A-->>G: Gültig
    G->>T: Task erstellen
    T->>DB: Task einfügen
    DB-->>T: Task ID
    T-->>G: Task erstellt
    G-->>D: Response
    D-->>U: UI aktualisieren
```

## Design-Patterns

### 1. **Microservices Pattern**
- Jeder Service ist unabhängig deploybar
- Services kommunizieren via REST APIs
- Lose Kopplung, hohe Kohäsion

### 2. **API Gateway Pattern**
- Einzelner Eingangspunkt für alle Clients
- Request-Routing und Load Balancing
- Querschnittsfunktionen (Auth, Logging)

### 3. **Repository Pattern**
- Datenbank-Abstraktion
- Konsistente Schnittstelle für Datenoperationen
- Einfaches Testen und Mocking

### 4. **Event-Driven Architecture**
- WebSocket für Echtzeit-Updates
- Event Sourcing für Audit Trail
- Asynchrone Verarbeitung

## Sicherheits-Architektur

```mermaid
graph LR
    subgraph "Sicherheits-Schichten"
        C[Client] --> TLS[TLS/HTTPS]
        TLS --> WAF[Web Application Firewall]
        WAF --> GW[API Gateway]
        GW --> AUTH[Auth Middleware]
        AUTH --> SVC[Services]
    end
    
    subgraph "Sicherheits-Features"
        JWT[JWT Tokens]
        RBAC[Rollenbasierter Zugriff]
        ENC[Verschlüsselung im Ruhezustand]
        AUD[Audit-Protokollierung]
    end
```

## Deployment-Architektur

```yaml
version: '3.8'
services:
  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
      
  task-service:
    build: ./backend/task-service
    environment:
      - DB_HOST=postgres
      - REDIS_HOST=redis
    depends_on:
      - postgres
      - redis
      
  auth-service:
    build: ./backend/auth-service
    environment:
      - JWT_SECRET=${JWT_SECRET}
      - DB_HOST=postgres
      
  postgres:
    image: postgres:14
    volumes:
      - postgres_data:/var/lib/postgresql/data
      
  redis:
    image: redis:alpine
    volumes:
      - redis_data:/data
```

## Skalierbarkeits-Überlegungen

1. **Horizontale Skalierung**: Services können hinter Load Balancer repliziert werden
2. **Datenbank-Sharding**: PostgreSQL unterstützt Partitionierung für große Datensätze
3. **Caching-Strategie**: Redis für Session- und häufig abgerufene Daten
4. **Asynchrone Verarbeitung**: Task-Queues für lang andauernde Operationen

## Monitoring & Observability

- **Metriken**: Prometheus + Grafana
- **Protokollierung**: ELK Stack (Elasticsearch, Logstash, Kibana)
- **Tracing**: OpenTelemetry
- **Health Checks**: In jeden Service integriert

## Zukünftige Verbesserungen

1. **GraphQL Gateway**: Für flexible Client-Abfragen
2. **Service Mesh**: Istio für erweiterte Traffic-Verwaltung
3. **Event Streaming**: Apache Kafka für Echtzeit-Daten-Pipeline
4. **ML Pipeline**: Dedizierter Service für KI-Model-Management