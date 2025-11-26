# Toasty

The smart, context-aware AI code reviewer from OWASP BLT.

## Overview

Toasty (BLT-AIBot) is a GitHub App that provides AI-powered code reviews and issue analysis. It uses:
- **Gemini AI** for intelligent code analysis and response generation
- **Qdrant Vector DB** for semantic code search and context retrieval
- **Celery** for background task processing
- **Redis** for caching and message brokering

## Features

- Automated PR code reviews with context-aware analysis
- Issue planning and resolution suggestions
- Responsive to @mentions in issue/PR comments
- Repository code indexing for semantic search
- Static analysis integration (Bandit, Ruff)

## Setup

### Prerequisites

- Python 3.11+
- Docker and Docker Compose
- A GitHub App configured with appropriate permissions
- Gemini API key
- Qdrant instance

### Environment Variables

Copy `.env.example` to `.env` and configure the following variables:

```bash
# Django
SECRET_KEY=your-secret-key-here

# PostgreSQL
POSTGRES_USER=toasty
POSTGRES_DB=toasty
POSTGRES_PASSWORD=your-password

# GitHub AIBot Configuration
GITHUB_AIBOT_APP_NAME=your-app-name
GITHUB_AIBOT_APP_ID=your-app-id
GITHUB_AIBOT_PRIVATE_KEY_B64=your-private-key-base64
GITHUB_AIBOT_WEBHOOK_SECRET=your-webhook-secret

# Gemini AI Configuration
GEMINI_API_KEY=your-gemini-api-key
GEMINI_GENERATION_MODEL=gemini-model-name
GEMINI_EMBEDDING_MODEL=gemini-embedding-model-name

# Redis and Celery Configuration
REDIS_URL=redis://redis:6379/0
CELERY_BROKER_URL=redis://redis:6379/0
CELERY_RESULT_BACKEND=redis://redis:6379/0

# Qdrant Vector DB Configuration
QDRANT_HOST=qdrant
QDRANT_VECTOR_SIZE=768
QDRANT_HTTP_PORT=6333
```

### Running with Docker Compose

```bash
docker-compose up --build
```

This starts:
- Web server (Django)
- PostgreSQL database
- Redis cache
- Celery worker
- Qdrant vector database

### Development Setup

```bash
# Install dependencies
poetry install

# Run migrations
poetry run python manage.py migrate

# Start development server
poetry run python manage.py runserver
```

## API Endpoints

- `POST /aibot/` - GitHub webhook endpoint
- `GET /aibot/health/` - Health check endpoint

## License

AGPL-3.0
