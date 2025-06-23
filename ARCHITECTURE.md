# ELWOSA System Architecture

## Overview

ELWOSA implements a modern microservices architecture designed for scalability, maintainability, and extensibility. The system follows Domain-Driven Design (DDD) principles and implements various enterprise patterns.

## System Components

```mermaid
graph TB
    subgraph "Frontend Layer"
        UI[React Dashboard]
        MW[Mobile Web App]
    end
    
    subgraph "API Gateway"
        GW[NGINX Reverse Proxy]
    end
    
    subgraph "Service Layer"
        TS[Task Service<br/>FastAPI:8001]
        AS[Auth Service<br/>FastAPI:8003]
        MS[Memory Service<br/>WebSocket:8765]
        AI[AI Bridge Service<br/>FastAPI:8006]
    end
    
    subgraph "Data Layer"
        PG[(PostgreSQL<br/>Tasks & Users)]
        CACHE[(Redis Cache<br/>Sessions)]
        MEM[(Memory Store<br/>JSON)]
    end
    
    subgraph "External Services"
        GPT[OpenAI API]
        LLM[Local LLMs]
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

## Core Services

### Task Management Service
- **Technology**: Python FastAPI
- **Port**: 8001
- **Responsibilities**:
  - CRUD operations for tasks
  - Priority management
  - Step tracking
  - Real-time updates

### Authentication Service
- **Technology**: Python FastAPI
- **Port**: 8003
- **Features**:
  - JWT token generation
  - User management
  - Role-based access control
  - Session management via Redis

### Memory Service
- **Technology**: Python WebSocket Server
- **Port**: 8765
- **Purpose**: Persistent system memory for AI context
- **Features**:
  - Real-time memory updates
  - Context preservation
  - WebSocket streaming

### AI Bridge Service
- **Technology**: Python FastAPI
- **Port**: 8006
- **Capabilities**:
  - Multi-model support (GPT-4, Llama, etc.)
  - Streaming responses
  - Context management
  - Load balancing

## Data Flow

```mermaid
sequenceDiagram
    participant U as User
    participant D as Dashboard
    participant G as Gateway
    participant T as Task Service
    participant A as Auth Service
    participant DB as PostgreSQL
    
    U->>D: Login Request
    D->>G: POST /auth/login
    G->>A: Authenticate
    A->>DB: Verify Credentials
    DB-->>A: User Data
    A-->>G: JWT Token
    G-->>D: Auth Response
    D-->>U: Dashboard Access
    
    U->>D: Create Task
    D->>G: POST /tasks
    G->>A: Verify Token
    A-->>G: Valid
    G->>T: Create Task
    T->>DB: Insert Task
    DB-->>T: Task ID
    T-->>G: Task Created
    G-->>D: Response
    D-->>U: Update UI
```

## Design Patterns

### 1. **Microservices Pattern**
- Each service is independently deployable
- Services communicate via REST APIs
- Loose coupling, high cohesion

### 2. **API Gateway Pattern**
- Single entry point for all clients
- Request routing and load balancing
- Cross-cutting concerns (auth, logging)

### 3. **Repository Pattern**
- Data access abstraction
- Consistent interface for data operations
- Easy testing and mocking

### 4. **Event-Driven Architecture**
- WebSocket for real-time updates
- Event sourcing for audit trail
- Asynchronous processing

## Security Architecture

```mermaid
graph LR
    subgraph "Security Layers"
        C[Client] --> TLS[TLS/HTTPS]
        TLS --> WAF[Web Application Firewall]
        WAF --> GW[API Gateway]
        GW --> AUTH[Auth Middleware]
        AUTH --> SVC[Services]
    end
    
    subgraph "Security Features"
        JWT[JWT Tokens]
        RBAC[Role-Based Access]
        ENC[Encryption at Rest]
        AUD[Audit Logging]
    end
```

## Deployment Architecture

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

## Scalability Considerations

1. **Horizontal Scaling**: Services can be replicated behind load balancer
2. **Database Sharding**: PostgreSQL supports partitioning for large datasets
3. **Caching Strategy**: Redis for session and frequently accessed data
4. **Async Processing**: Task queues for long-running operations

## Monitoring & Observability

- **Metrics**: Prometheus + Grafana
- **Logging**: ELK Stack (Elasticsearch, Logstash, Kibana)
- **Tracing**: OpenTelemetry
- **Health Checks**: Built into each service

## Future Enhancements

1. **GraphQL Gateway**: For flexible client queries
2. **Service Mesh**: Istio for advanced traffic management
3. **Event Streaming**: Apache Kafka for real-time data pipeline
4. **ML Pipeline**: Dedicated service for AI model management