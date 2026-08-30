# Template API

A reusable Django REST Framework backend template for building scalable, maintainable, and production-oriented REST APIs.

This template provides a structured backend foundation with authentication, JWT, standardized responses, centralized exception handling, service and selector layers, Redis-backed idempotency, query filtering/search/ordering, pagination, file validation, and cloud storage.

The goal is to eliminate repetitive backend setup and provide a consistent architecture that can be reused across future projects.

---

# Features

- Django REST Framework
- Layered architecture
- Service Layer
- Selector Layer
- JWT authentication
- Registration and login
- Refresh token support
- Email verification support
- User profile management
- Standardized API responses
- Centralized exception handling
- Exception mapping
- Redis integration
- Redis-backed idempotency middleware
- Request deduplication
- Idempotent response replay
- API throttling
- Query filtering
- Search
- Ordering
- Pagination(cursor, pagenumber)
- Database query optimization
- File validation
- Cloudinary storage
- Storage abstraction
- UUID primary keys
- Timestamp models
- Environment-based configuration
- API URL versioning
- Audit logging

---


# Architecture

The template follows a **Modular Monolith architecture with layered architecture inside each feature module**.

The application is organized around business features, with each feature owning its own views, serializers, services, selectors, and models.

Each feature follows a layered structure:

```text
Feature Module
│
├── Views
│      → Presentation / HTTP layer
│
├── Serializers
│      → Validation / API boundary
│
├── Services
│      → Business / Application logic
│
├── Selectors
│      → Data access / Query logic
│
└── Models
       → Persistence / Database layer
```


# Architectural Overview
```text

                         HTTP Request
                              │
                              ▼
                       Middleware Layer
                              │
                 ┌────────────┴────────────┐
                 │                         │
            Idempotency               Throttling
                 │                         │
                 └────────────┬────────────┘
                              │
                              ▼
                           API View
                              │
                    ┌─────────┴─────────┐
                    │                   │
             BaseModelViewSet      Custom View
                    │                   │
                    ▼                   ▼
               Serializer          Serializer
                    │                   │
                    ▼                   ▼
              Generic CRUD           Service
                    │             /           \
                    │            /             \
                    │           ▼               ▼
                    │       Selector       Infrastructure
                    │           │          /    │    │    \
                    │           │         /     │    │     \
                    │           ▼        ▼      ▼    ▼      ▼
                    │       Database   Redis  Storage Email
                    │                         │
                    │                         ▼
                    │                     Cloudinary
                    │
                    ▼
                 Response
                 
```

# Roadmap

Potential future additions:

- OpenAPI / Swagger documentation
- Structured logging
- Health check endpoints
- Docker configuration
- CI/CD pipeline
- Automated testing pipeline
- Celery integration
- Background task processing
- Advanced caching
- Role and permission system
- Observability
- Production deployment configuration
- PostgreSQL support

---

# Status

**Template API — Initial Template Complete**

This template provides the core backend infrastructure required to start new Django REST Framework projects with a consistent architecture.

It is intended to serve as a reusable starting point for future applications rather than as a standalone business application.

---
