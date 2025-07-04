# ELWOSA API Documentation

Welcome to the ELWOSA API documentation. Our platform provides comprehensive REST APIs for all system components.

## Available APIs

### Core Services

1. **[Task API](./task-api.md)** - Task management and workflow automation
   - Create, read, update, and delete tasks
   - Priority-based organization
   - Real-time status updates
   - Step tracking for task progress

2. **[Memory API](./memory-api.md)** - Persistent storage for AI interactions
   - Store important decisions and milestones
   - Full-text search capabilities
   - Tag-based categorization
   - Cross-reference with tasks

3. **[AI Bridge API](./ai-bridge-api.md)** - Unified AI model integration
   - Support for OpenAI and Ollama
   - Streaming responses
   - Context management
   - Multiple AI personalities

4. **[Auth API](./auth-api.md)** - Authentication and authorization
   - JWT token management
   - User authentication
   - Role-based access control
   - Session management

## API Standards

All ELWOSA APIs follow these standards:

- **REST principles** with predictable resource-oriented URLs
- **JSON** request and response bodies
- **HTTP status codes** to indicate success or failure
- **CORS enabled** for browser-based access
- **OpenAPI 3.0** specification compliance

## Authentication

Most endpoints require authentication via JWT tokens:

```http
Authorization: Bearer <your-jwt-token>
```

Obtain tokens through the Auth API's `/login` endpoint.

## Base URLs

- **Production**: `https://api.elwosa.com`
- **Development**: `http://localhost:{service-port}`

Service ports:
- Task API: 8001
- Memory API: 8765
- AI Bridge: 8006
- Auth API: 8003

## Rate Limiting

API calls are rate-limited to ensure service stability:
- Authenticated requests: 1000/hour
- Unauthenticated requests: 100/hour

## Error Handling

All APIs return consistent error responses:

```json
{
  "error": {
    "code": "RESOURCE_NOT_FOUND",
    "message": "The requested task was not found",
    "details": {
      "task_id": 12345
    }
  }
}
```

## Getting Started

1. Set up authentication by obtaining a JWT token
2. Choose the appropriate API for your use case
3. Make requests following the API documentation
4. Handle responses and errors appropriately

## Support

For API support or questions:
- Check the individual API documentation
- Review our [examples repository](https://github.com/MadGapun/ELWOSA-Examples)
- Open an issue on [GitHub](https://github.com/MadGapun/ELWOSA-Pub/issues)
