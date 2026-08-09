# AI Security Copilot

AI Security Copilot is a FastAPI-based security assistant for ingesting vulnerability scanner exports, normalizing findings, tracking remediation state, and answering security questions with a retrieval-augmented Azure OpenAI workflow.

## Core capabilities

- JWT authentication with access/refresh token flow
- Role-based access control for security operations
- CSV/JSON vulnerability scan upload and background processing
- Scanner detection and normalization for Wiz and Tenable-style data
- Vulnerability listing, filtering, detail lookup, and status updates
- Document ingestion for RAG context
- Azure OpenAI chat and streaming chat endpoints
- Input/output security pipeline, prompt-injection checks, and PII controls
- Conversation history and audit logging
- LLM latency/token logging and RAG evaluation support
- PostgreSQL/SQLAlchemy/Alembic persistence with pgvector support
- Redis-backed application services and API rate limiting
- Docker/Docker Compose configuration

## Architecture

```text
Client
  |
  v
FastAPI API (/api/v1)
  |-- Auth / RBAC
  |-- Vulnerability Scan Upload
  |     -> Background Scan Worker
  |     -> Parser -> Scanner Detector -> Normalizer
  |     -> Vulnerability Service -> PostgreSQL
  |
  |-- Document Upload
  |     -> Chunking -> Embeddings -> pgvector
  |
  `-- Chat / Streaming Chat
        -> AI Security Pipeline
        -> Retriever / Reranker
        -> Prompt Builder
        -> Azure OpenAI
        -> Output Security
        -> Audit + Monitoring
```

## Main API routes

All routes are under `/api/v1`.

- `GET /health`
- `POST /auth/register`
- `POST /auth/login`
- `POST /auth/refresh`
- `POST /auth/logout`
- `GET /users/me`
- `POST /vulnerabilities/upload`
- `GET /vulnerabilities/scans/{scan_id}`
- `GET /vulnerabilities/scans`
- `GET /vulnerabilities`
- `GET /vulnerabilities/{vulnerability_id}`
- `PATCH /vulnerabilities/{vulnerability_id}/status`
- `POST /documents/upload`
- `POST /chat`
- `POST /chat/stream`
- `POST /evaluation/run`

Interactive API documentation is available at `/docs` when the app is running.

## Local setup

Use Python 3.12+.

```bash
python -m venv .venv
```

Activate the virtual environment, then install dependencies:

```bash
pip install -r requirements.txt
```

Create the local environment file:

```bash
cp .env.example .env
```

Configure PostgreSQL, Redis, Azure OpenAI, and LangSmith values as needed. Never commit `.env` or real credentials.

Apply migrations:

```bash
alembic upgrade head
```

Start the API:

```bash
uvicorn app.main:app --reload
```

## Tests

Run the lightweight project smoke checks with:

```bash
pytest -q
```

A syntax-only verification can also be run with:

```bash
python -m compileall -q app test
```

## Docker

Docker assets are included for deployment-capable environments:

```bash
docker compose up --build
```

Docker runtime validation is environment-dependent and is not required for the lightweight local verification flow.

## Security notes

- Keep `.env` out of source control.
- Rotate any credential that has been exposed outside its intended secret store.
- Use strong JWT secrets in non-development environments.
- Restrict Azure OpenAI, database, Redis, and LangSmith credentials to least privilege.

## Project status

Core application development is complete. The repository includes authentication/RBAC, vulnerability ingestion and normalization, RAG chat, AI security controls, monitoring/evaluation components, database migrations, tests, and deployment configuration.
