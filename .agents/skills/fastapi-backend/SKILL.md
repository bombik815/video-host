---
name: fastapi-backend
description: FastAPI backend development standards. Use when generating, modifying, or reviewing FastAPI, SQLAlchemy, Alembic, PostgreSQL, Pydantic v2 backend code, endpoints, models, migrations, services, repositories, tests, Dockerfiles.
---

# SKILL: FastAPI Backend Development
> **Operational instruction manual for Claude Code.**
> Read this file before generating, modifying, or reviewing any backend code in this project.

---

## Mission

This skill governs all backend code generation, modification, and maintenance for a production-grade REST API service built with FastAPI, PostgreSQL, SQLAlchemy 2.x, and Pydantic v2. Follow every rule here precisely. Prefer explicitness over cleverness. Prefer boring, correct, and maintainable over novel and brittle.

---

## Table of Contents

1. [Project Structure](#1-project-structure)
2. [Naming Conventions](#2-naming-conventions)
3. [Coding Standards](#3-coding-standards)
4. [FastAPI Conventions](#4-fastapi-conventions)
5. [Endpoint Design](#5-endpoint-design)
6. [Schema / Model / Service / Repository Separation](#6-schema--model--service--repository-separation)
7. [Database Design & Migrations](#7-database-design--migrations)
8. [Configuration & Secrets](#8-configuration--secrets)
9. [Authentication-Aware Patterns](#9-authentication-aware-patterns)
10. [Validation & Error Handling](#10-validation--error-handling)
11. [Testing Standards](#11-testing-standards)
12. [Logging & Observability](#12-logging--observability)
13. [Docker & Containerization](#13-docker--containerization)
14. [Async Usage](#14-async-usage)
15. [Background Tasks](#15-background-tasks)
16. [Retry-Safe & Idempotent Behavior](#16-retry-safe--idempotent-behavior)
17. [Security Defaults](#17-security-defaults)
18. [Performance & Scalability](#18-performance--scalability)
19. [Deployment Readiness Checklist](#19-deployment-readiness-checklist)
20. [Anti-Patterns to Avoid](#20-anti-patterns-to-avoid)
21. [Definition of Done](#21-definition-of-done)

---

## 1. Project Structure

Always scaffold new projects and modules according to this layout. Never deviate without explicit instruction.

```
project-root/
├── app/
│   ├── __init__.py
│   ├── main.py                  # FastAPI app factory, lifespan, router registration
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py            # Pydantic Settings — single source of truth
│   │   ├── security.py          # Password hashing, JWT encode/decode
│   │   ├── dependencies.py      # Shared FastAPI Depends() callables
│   │   └── exceptions.py        # Custom exception classes
│   ├── db/
│   │   ├── __init__.py
│   │   ├── base.py              # DeclarativeBase, metadata
│   │   ├── session.py           # Async engine, sessionmaker, get_db dependency
│   │   └── models/              # SQLAlchemy ORM models, one file per domain
│   │       ├── __init__.py
│   │       └── user.py
│   ├── api/
│   │   ├── __init__.py
│   │   └── v1/
│   │       ├── __init__.py
│   │       ├── router.py        # Aggregates all v1 sub-routers
│   │       └── endpoints/       # One file per resource
│   │           ├── __init__.py
│   │           ├── users.py
│   │           └── health.py
│   ├── schemas/                 # Pydantic v2 request/response schemas
│   │   ├── __init__.py
│   │   └── user.py
│   ├── services/                # Business logic, orchestration
│   │   ├── __init__.py
│   │   └── user_service.py
│   ├── repositories/            # All database queries
│   │   ├── __init__.py
│   │   └── user_repository.py
│   └── workers/                 # Background tasks / ARQ / Celery workers
│       └── __init__.py
├── alembic/
│   ├── env.py
│   ├── script.py.mako
│   └── versions/
├── tests/
│   ├── conftest.py
│   ├── unit/
│   │   └── services/
│   └── integration/
│       └── api/
│           └── v1/
├── scripts/                     # One-off admin/maintenance scripts
├── .env.example                 # Committed — no real secrets
├── .env                         # Not committed
├── alembic.ini
├── docker-compose.yml
├── docker-compose.override.yml  # Local dev overrides
├── Dockerfile
├── pyproject.toml
└── README.md
```

### Module Generation Rules

When adding a new resource (e.g., `orders`):
1. Create `app/db/models/order.py` — ORM model.
2. Create `app/schemas/order.py` — Pydantic schemas.
3. Create `app/repositories/order_repository.py` — DB queries only.
4. Create `app/services/order_service.py` — business logic, calls repository.
5. Create `app/api/v1/endpoints/orders.py` — HTTP layer, calls service.
6. Register router in `app/api/v1/router.py`.
7. Generate Alembic migration.
8. Add tests in `tests/unit/services/test_order_service.py` and `tests/integration/api/v1/test_orders.py`.

---

## 2. Naming Conventions

| Concept | Convention | Example |
|---|---|---|
| Python files | `snake_case.py` | `user_service.py` |
| Classes | `PascalCase` | `UserService` |
| Functions / methods | `snake_case` | `get_user_by_email` |
| Variables | `snake_case` | `current_user` |
| Constants | `UPPER_SNAKE_CASE` | `MAX_PAGE_SIZE` |
| Pydantic schemas | `PascalCase` + suffix | `UserCreate`, `UserRead`, `UserUpdate` |
| ORM models | `PascalCase`, singular | `User`, `Order` |
| DB tables | `snake_case`, plural | `users`, `orders` |
| DB columns | `snake_case` | `created_at`, `hashed_password` |
| API endpoints | `kebab-case`, plural nouns | `/api/v1/users`, `/api/v1/order-items` |
| Path parameters | `snake_case` | `user_id`, `order_id` |
| Environment variables | `UPPER_SNAKE_CASE` | `DATABASE_URL`, `SECRET_KEY` |
| Alembic revisions | descriptive slug | `add_orders_table`, `add_user_is_active` |

---

## 3. Coding Standards

### Python Version & Typing

- Target **Python 3.12+**. Use all modern typing features.
- All functions, methods, and class attributes **must** have type annotations. No `Any` unless absolutely necessary and explicitly commented.
- Use `from __future__ import annotations` only when needed for forward references; prefer native `X | Y` union syntax.
- Use `TypeAlias` for complex repeated types.

```python
# Correct
async def get_user(user_id: int, db: AsyncSession) -> User | None:
    ...

# Wrong — missing return type, no param types
async def get_user(user_id, db):
    ...
```

### Style

- Follow **PEP 8**. Use `ruff` for linting and formatting (replaces `black` + `isort` + `flake8`).
- Max line length: **100 characters**.
- Imports order: stdlib → third-party → local. Always use absolute imports within `app/`.
- No wildcard imports (`from module import *`).
- No mutable default arguments.

### `pyproject.toml` Tooling Config (include this)

```toml
[tool.ruff]
line-length = 100
target-version = "py312"

[tool.ruff.lint]
select = ["E", "F", "I", "UP", "B", "SIM", "TCH"]
ignore = ["E501"]

[tool.mypy]
python_version = "3.12"
strict = true
ignore_missing_imports = true
```

---

## 4. FastAPI Conventions

### App Factory (`app/main.py`)

Always use the **lifespan** context manager. Never use deprecated `on_event` decorators.

```python
from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.api.v1.router import v1_router
from app.core.config import settings
from app.db.session import engine


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    yield
    # Shutdown
    await engine.dispose()


def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.PROJECT_NAME,
        version=settings.API_VERSION,
        openapi_url=f"{settings.API_V1_STR}/openapi.json",
        docs_url=f"{settings.API_V1_STR}/docs",
        lifespan=lifespan,
    )
    app.include_router(v1_router, prefix=settings.API_V1_STR)
    return app


app = create_app()
```

### Dependency Injection

- All shared state (DB session, current user, config) is injected via `Depends()`.
- Never import `settings` or instantiate services inside endpoint handlers — inject them.
- Define reusable dependencies in `app/core/dependencies.py`.

```python
# app/core/dependencies.py
from typing import Annotated
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db

DBSession = Annotated[AsyncSession, Depends(get_db)]
```

### Router Registration

```python
# app/api/v1/router.py
from fastapi import APIRouter
from app.api.v1.endpoints import users, health

v1_router = APIRouter()
v1_router.include_router(health.router, prefix="/health", tags=["health"])
v1_router.include_router(users.router, prefix="/users", tags=["users"])
```

---

## 5. Endpoint Design

### REST Principles

- Use plural nouns for resources: `/users`, `/orders`, `/products`.
- Use HTTP verbs correctly:
  - `GET` — read, never mutates state
  - `POST` — create a new resource
  - `PUT` — full replacement of a resource
  - `PATCH` — partial update
  - `DELETE` — remove a resource
- Return appropriate HTTP status codes:
  - `200` — OK (GET, PATCH, PUT success)
  - `201` — Created (POST success, include `Location` header)
  - `204` — No Content (DELETE success)
  - `400` — Validation error / bad request
  - `401` — Unauthenticated
  - `403` — Forbidden
  - `404` — Not found
  - `409` — Conflict (duplicate resource)
  - `422` — Unprocessable entity (Pydantic validation failure, auto-handled)
  - `500` — Internal server error (never expose stack traces)

### API Versioning

- All routes live under `/api/v1/`. Version in the URL prefix only.
- When breaking changes are required, add `/api/v2/` — never modify v1 contracts.
- `settings.API_V1_STR = "/api/v1"`

### Pagination, Filtering, Sorting

Always implement pagination on list endpoints. Use offset-based pagination by default.

```python
# app/schemas/common.py
from pydantic import BaseModel, Field

class PaginationParams(BaseModel):
    page: int = Field(default=1, ge=1)
    page_size: int = Field(default=20, ge=1, le=100)

    @property
    def offset(self) -> int:
        return (self.page - 1) * self.page_size

class PaginatedResponse[T](BaseModel):
    items: list[T]
    total: int
    page: int
    page_size: int
    pages: int
```

- Filtering: Accept filter params as query parameters. Define explicit typed query params — no raw dict unpacking.
- Sorting: Accept `sort_by` (field name allowlist) and `sort_order` (`asc` | `desc`).
- Max `page_size`: **100**. Enforce in schema with `le=100`.

### Endpoint Template

```python
# app/api/v1/endpoints/users.py
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from app.core.dependencies import DBSession, CurrentUser
from app.schemas.user import UserCreate, UserRead, UserUpdate
from app.schemas.common import PaginatedResponse, PaginationParams
from app.services.user_service import UserService

router = APIRouter()


@router.get("", response_model=PaginatedResponse[UserRead])
async def list_users(
    db: DBSession,
    pagination: Annotated[PaginationParams, Depends()],
    current_user: CurrentUser,
) -> PaginatedResponse[UserRead]:
    return await UserService(db).list_users(pagination)


@router.get("/{user_id}", response_model=UserRead)
async def get_user(user_id: int, db: DBSession, current_user: CurrentUser) -> UserRead:
    user = await UserService(db).get_by_id(user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return UserRead.model_validate(user)


@router.post("", response_model=UserRead, status_code=status.HTTP_201_CREATED)
async def create_user(payload: UserCreate, db: DBSession) -> UserRead:
    return await UserService(db).create_user(payload)


@router.patch("/{user_id}", response_model=UserRead)
async def update_user(
    user_id: int, payload: UserUpdate, db: DBSession, current_user: CurrentUser
) -> UserRead:
    return await UserService(db).update_user(user_id, payload)


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: int, db: DBSession, current_user: CurrentUser) -> None:
    await UserService(db).delete_user(user_id)
```

### Health Endpoint (always include)

```python
# app/api/v1/endpoints/health.py
from fastapi import APIRouter, Depends
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db

router = APIRouter()


@router.get("/live")
async def liveness() -> dict[str, str]:
    return {"status": "ok"}


@router.get("/ready")
async def readiness(db: AsyncSession = Depends(get_db)) -> dict[str, str]:
    await db.execute(text("SELECT 1"))
    return {"status": "ready"}
```

---

## 6. Schema / Model / Service / Repository Separation

This is the core architectural boundary. Never cross layers.

### Layer Responsibilities

| Layer | Location | Responsibility | May Import |
|---|---|---|---|
| **ORM Model** | `app/db/models/` | DB table mapping only | SQLAlchemy, `app.db.base` |
| **Schema** | `app/schemas/` | Validation, serialization | Pydantic only |
| **Repository** | `app/repositories/` | All SQL queries | ORM models, SQLAlchemy, `AsyncSession` |
| **Service** | `app/services/` | Business logic, transactions | Repository, schemas, exceptions |
| **Endpoint** | `app/api/v1/endpoints/` | HTTP interface | Service, schemas, dependencies |

### ORM Model Pattern

```python
# app/db/models/user.py
from datetime import datetime
from sqlalchemy import String, Boolean, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column
from app.db.base import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    is_superuser: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False
    )
```

### Schema Pattern

```python
# app/schemas/user.py
from datetime import datetime
from pydantic import BaseModel, EmailStr, Field, ConfigDict


class UserBase(BaseModel):
    email: EmailStr
    is_active: bool = True


class UserCreate(UserBase):
    password: str = Field(min_length=8, max_length=128)


class UserUpdate(BaseModel):
    email: EmailStr | None = None
    is_active: bool | None = None
    password: str | None = Field(default=None, min_length=8, max_length=128)


class UserRead(UserBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    is_superuser: bool
    created_at: datetime
    updated_at: datetime
```

### Repository Pattern

```python
# app/repositories/user_repository.py
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.models.user import User
from app.schemas.common import PaginationParams


class UserRepository:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def get_by_id(self, user_id: int) -> User | None:
        result = await self.db.execute(select(User).where(User.id == user_id))
        return result.scalar_one_or_none()

    async def get_by_email(self, email: str) -> User | None:
        result = await self.db.execute(select(User).where(User.email == email))
        return result.scalar_one_or_none()

    async def list_with_count(self, pagination: PaginationParams) -> tuple[list[User], int]:
        count_q = select(func.count()).select_from(User)
        total = (await self.db.execute(count_q)).scalar_one()
        items_q = select(User).offset(pagination.offset).limit(pagination.page_size)
        items = list((await self.db.execute(items_q)).scalars().all())
        return items, total

    async def create(self, user: User) -> User:
        self.db.add(user)
        await self.db.flush()
        await self.db.refresh(user)
        return user

    async def delete(self, user: User) -> None:
        await self.db.delete(user)
```

### Service Pattern

```python
# app/services/user_service.py
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status
from app.core.security import get_password_hash
from app.db.models.user import User
from app.repositories.user_repository import UserRepository
from app.schemas.user import UserCreate, UserRead, UserUpdate
from app.schemas.common import PaginationParams, PaginatedResponse


class UserService:
    def __init__(self, db: AsyncSession) -> None:
        self.repo = UserRepository(db)
        self.db = db

    async def get_by_id(self, user_id: int) -> User | None:
        return await self.repo.get_by_id(user_id)

    async def list_users(self, pagination: PaginationParams) -> PaginatedResponse[UserRead]:
        items, total = await self.repo.list_with_count(pagination)
        pages = (total + pagination.page_size - 1) // pagination.page_size
        return PaginatedResponse(
            items=[UserRead.model_validate(u) for u in items],
            total=total,
            page=pagination.page,
            page_size=pagination.page_size,
            pages=pages,
        )

    async def create_user(self, payload: UserCreate) -> UserRead:
        existing = await self.repo.get_by_email(payload.email)
        if existing:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already registered")
        user = User(
            email=payload.email,
            hashed_password=get_password_hash(payload.password),
        )
        created = await self.repo.create(user)
        await self.db.commit()
        return UserRead.model_validate(created)

    async def update_user(self, user_id: int, payload: UserUpdate) -> UserRead:
        user = await self.repo.get_by_id(user_id)
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        update_data = payload.model_dump(exclude_unset=True)
        if "password" in update_data:
            update_data["hashed_password"] = get_password_hash(update_data.pop("password"))
        for field, value in update_data.items():
            setattr(user, field, value)
        await self.db.commit()
        await self.db.refresh(user)
        return UserRead.model_validate(user)

    async def delete_user(self, user_id: int) -> None:
        user = await self.repo.get_by_id(user_id)
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        await self.repo.delete(user)
        await self.db.commit()
```

**Transaction boundary rule**: `commit()` and `rollback()` live in the **service layer only**. Repositories never commit. Endpoints never commit.

---

## 7. Database Design & Migrations

### SQLAlchemy 2.x Setup

```python
# app/db/base.py
from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    pass
```

```python
# app/db/session.py
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from app.core.config import settings

engine = create_async_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True,
    pool_size=10,
    max_overflow=20,
    echo=settings.DB_ECHO,
)

AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    autocommit=False,
    autoflush=False,
    expire_on_commit=False,
)


async def get_db() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
```

### Database Design Rules

- Every table must have: `id` (integer PK or UUID), `created_at`, `updated_at`.
- Use `UUID` PKs for publicly exposed resources; integer PKs for internal join tables.
- Always define explicit `__tablename__`.
- Index all foreign keys and columns used in `WHERE` clauses.
- Use `nullable=False` by default. Only allow NULL when the domain truly requires it.
- Use `String(n)` with explicit lengths, not unbound `Text` unless appropriate.
- Use `DateTime(timezone=True)` for all timestamps. Store UTC everywhere.
- Use `Enum` types in Python and map to DB `VARCHAR` or Postgres native `ENUM` consistently.
- Soft-delete pattern: add `deleted_at: Mapped[datetime | None]` and filter in repository.

### Alembic Migration Discipline

**Always** generate migrations via Alembic. Never apply schema changes manually.

```bash
# Generate migration
alembic revision --autogenerate -m "add_orders_table"

# Review generated file before applying — always check it
# Apply
alembic upgrade head

# Rollback one step
alembic downgrade -1
```

- **Always review** autogenerated migration files before committing. Alembic misses: index changes on existing data, column type changes needing casting, dropped columns in use by other services.
- Every migration must have a working `downgrade()` function.
- Migrations are immutable once merged to `main`. Never edit a committed migration.
- Migration files are committed to version control.
- `alembic/env.py` must import all models so autogenerate detects them:

```python
# alembic/env.py (relevant section)
from app.db.base import Base
from app.db.models import user, order  # noqa: F401 — import all models here

target_metadata = Base.metadata
```

---

## 8. Configuration & Secrets

### Pydantic Settings

```python
# app/core/config.py
from pydantic import PostgresDsn, field_validator, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", case_sensitive=True)

    PROJECT_NAME: str = "MyAPI"
    API_VERSION: str = "0.1.0"
    API_V1_STR: str = "/api/v1"
    ENVIRONMENT: str = "development"  # development | staging | production
    DEBUG: bool = False
    DB_ECHO: bool = False

    DATABASE_URL: PostgresDsn
    SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    ALGORITHM: str = "HS256"

    CORS_ORIGINS: list[str] = []

    @field_validator("SECRET_KEY")
    @classmethod
    def secret_key_min_length(cls, v: str) -> str:
        if len(v) < 32:
            raise ValueError("SECRET_KEY must be at least 32 characters")
        return v


settings = Settings()
```

### `.env.example` (always commit this)

```dotenv
PROJECT_NAME=MyAPI
ENVIRONMENT=development
DEBUG=false
DB_ECHO=false

DATABASE_URL=postgresql+asyncpg://postgres:postgres@localhost:5432/myapi

SECRET_KEY=change-me-to-a-random-32-char-minimum-string
ACCESS_TOKEN_EXPIRE_MINUTES=30

CORS_ORIGINS=["http://localhost:3000"]
```

### Rules

- `.env` is in `.gitignore`. Never commit real secrets.
- In production, inject secrets via environment variables or a secrets manager (Vault, AWS Secrets Manager). Never bake secrets into images.
- Use `pydantic-settings` — never use `os.getenv()` directly in application code.
- All config is validated at startup. If required variables are missing, the app fails immediately with a clear error.
- Never log secret values. Mask them in debug output.

---

## 9. Authentication-Aware Patterns

### JWT Dependency

```python
# app/core/dependencies.py
from typing import Annotated
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.security import decode_access_token
from app.db.session import get_db
from app.db.models.user import User
from app.repositories.user_repository import UserRepository

bearer_scheme = HTTPBearer()

DBSession = Annotated[AsyncSession, Depends(get_db)]


async def get_current_user(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(bearer_scheme)],
    db: DBSession,
) -> User:
    payload = decode_access_token(credentials.credentials)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    user = await UserRepository(db).get_by_id(int(payload["sub"]))
    if not user or not user.is_active:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Inactive user")
    return user


async def get_current_superuser(current_user: Annotated[User, Depends(get_current_user)]) -> User:
    if not current_user.is_superuser:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not enough permissions")
    return current_user


CurrentUser = Annotated[User, Depends(get_current_user)]
SuperUser = Annotated[User, Depends(get_current_superuser)]
```

### Security Rules

- Never store plaintext passwords. Use `bcrypt` via `passlib`.
- JWT `sub` claim must be the user's database ID (as string).
- Always validate token signature AND expiry.
- Refresh tokens must be rotated on use and stored server-side (in Redis or DB) for revocation support.
- Protect all state-mutating endpoints with `CurrentUser` by default. Opt out explicitly and document why.
- Rate-limit auth endpoints (`/login`, `/register`) using middleware.

---

## 10. Validation & Error Handling

### Global Exception Handler

```python
# app/main.py — add to create_app()
from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
import logging

logger = logging.getLogger(__name__)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
    return JSONResponse(
        status_code=422,
        content={"detail": exc.errors(), "body": exc.body},
    )


@app.exception_handler(Exception)
async def unhandled_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    logger.exception("Unhandled exception: %s", exc)
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"},
    )
```

### Custom Exceptions

```python
# app/core/exceptions.py
class AppError(Exception):
    def __init__(self, message: str, status_code: int = 400) -> None:
        self.message = message
        self.status_code = status_code
        super().__init__(message)

class NotFoundError(AppError):
    def __init__(self, resource: str, resource_id: int | str) -> None:
        super().__init__(f"{resource} with id {resource_id} not found", status_code=404)

class ConflictError(AppError):
    def __init__(self, message: str) -> None:
        super().__init__(message, status_code=409)
```

### Validation Rules

- Use Pydantic v2 `Field()` validators for all input constraints (min/max length, regex, value ranges).
- Use `model_validator` for cross-field validation.
- Never raise bare `Exception`. Always raise `HTTPException` or a custom `AppError`.
- Never expose internal error messages, stack traces, or SQL errors to clients in production.
- Validate path parameters are positive integers where applicable using `Annotated[int, Path(ge=1)]`.

---

## 11. Testing Standards

### Setup

```python
# tests/conftest.py
import asyncio
import pytest
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from app.main import app
from app.db.base import Base
from app.db.session import get_db
from app.core.config import settings

TEST_DATABASE_URL = str(settings.DATABASE_URL).replace("/myapi", "/myapi_test")

test_engine = create_async_engine(TEST_DATABASE_URL, echo=False)
TestSessionLocal = async_sessionmaker(test_engine, class_=AsyncSession, expire_on_commit=False)


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session", autouse=True)
async def setup_db():
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture
async def db() -> AsyncSession:
    async with TestSessionLocal() as session:
        yield session
        await session.rollback()


@pytest.fixture
async def client(db: AsyncSession) -> AsyncClient:
    async def override_get_db():
        yield db

    app.dependency_overrides[get_db] = override_get_db
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        yield ac
    app.dependency_overrides.clear()
```

### Test Rules

- **Unit tests** test services and repositories with a real test DB session. Mock external I/O only.
- **Integration tests** test endpoints via `httpx.AsyncClient`. Test the full HTTP contract.
- No `unittest.mock.patch` on SQLAlchemy internals. Use a real test database.
- Each test must be isolated — use DB rollback per test (via fixture).
- Test file names mirror source: `app/services/user_service.py` → `tests/unit/services/test_user_service.py`.
- Every endpoint must have tests for: happy path, 404, 422 (invalid input), 401 (if auth-protected).
- Minimum coverage target: **80%** on `app/` (enforced in CI).
- Use `pytest-asyncio` with `asyncio_mode = "auto"` in `pyproject.toml`.

```toml
[tool.pytest.ini_options]
asyncio_mode = "auto"
testpaths = ["tests"]
```

### Integration Test Example

```python
# tests/integration/api/v1/test_users.py
import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_create_user_success(client: AsyncClient) -> None:
    response = await client.post("/api/v1/users", json={"email": "test@example.com", "password": "securepass123"})
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "test@example.com"
    assert "hashed_password" not in data


@pytest.mark.asyncio
async def test_create_user_duplicate_email(client: AsyncClient) -> None:
    payload = {"email": "dup@example.com", "password": "securepass123"}
    await client.post("/api/v1/users", json=payload)
    response = await client.post("/api/v1/users", json=payload)
    assert response.status_code == 409
```

---

## 12. Logging & Observability

### Structured Logging Setup

```python
# app/core/logging.py
import logging
import sys
from app.core.config import settings


def configure_logging() -> None:
    log_level = logging.DEBUG if settings.DEBUG else logging.INFO
    handler = logging.StreamHandler(sys.stdout)

    if settings.ENVIRONMENT == "production":
        import json
        class JSONFormatter(logging.Formatter):
            def format(self, record: logging.LogRecord) -> str:
                return json.dumps({
                    "level": record.levelname,
                    "message": record.getMessage(),
                    "logger": record.name,
                    "time": self.formatTime(record),
                })
        handler.setFormatter(JSONFormatter())
    else:
        handler.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(name)s: %(message)s"))

    logging.basicConfig(level=log_level, handlers=[handler])
    logging.getLogger("sqlalchemy.engine").setLevel(logging.WARNING)
```

Call `configure_logging()` inside the `lifespan` startup block.

### Rules

- Log at `INFO` level: startup, shutdown, and meaningful business events.
- Log at `WARNING`: recoverable errors, retries, deprecated usage.
- Log at `ERROR`: unhandled exceptions, external service failures.
- **Never log**: passwords, tokens, PII, full request/response bodies.
- In production, always use JSON-formatted structured logs.
- Include `request_id` in log context for traceability. Use middleware to inject it.
- Add a `GET /api/v1/health/ready` endpoint that checks DB connectivity (see §5).
- Expose Prometheus metrics via `prometheus-fastapi-instrumentator` for production workloads.

---

## 13. Docker & Containerization

### Dockerfile

```dockerfile
# Dockerfile
FROM python:3.12-slim AS base

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

WORKDIR /app

FROM base AS builder
COPY pyproject.toml ./
RUN pip install uv && uv pip install --system --no-cache -e ".[prod]"

FROM base AS final
COPY --from=builder /usr/local/lib/python3.12 /usr/local/lib/python3.12
COPY --from=builder /usr/local/bin /usr/local/bin
COPY . .

RUN addgroup --gid 1001 appgroup && \
    adduser --uid 1001 --gid 1001 --no-create-home --disabled-password appuser && \
    chown -R appuser:appgroup /app

USER appuser

EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "1"]
```

### docker-compose.yml

```yaml
# docker-compose.yml
services:
  api:
    build: .
    ports:
      - "8000:8000"
    environment:
      DATABASE_URL: postgresql+asyncpg://postgres:postgres@db:5432/myapi
      SECRET_KEY: ${SECRET_KEY}
      ENVIRONMENT: development
      DEBUG: "true"
    depends_on:
      db:
        condition: service_healthy
    restart: unless-stopped

  db:
    image: postgres:16-alpine
    environment:
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres
      POSTGRES_DB: myapi
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 5s
      timeout: 5s
      retries: 5

volumes:
  postgres_data:
```

### docker-compose.override.yml (local dev only, not committed)

```yaml
# docker-compose.override.yml
services:
  api:
    volumes:
      - .:/app
    command: uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

### Containerization Rules

- Run as a non-root user in all stages.
- Use multi-stage builds to minimize image size.
- Use `service_healthy` conditions — never sleep-based startup waits.
- Pin base image versions (`python:3.12-slim`, `postgres:16-alpine`).
- Set `PYTHONDONTWRITEBYTECODE` and `PYTHONUNBUFFERED` in all images.
- Never bake `.env` files or secrets into images.
- Include a `.dockerignore` that excludes: `.env`, `__pycache__`, `.git`, `tests/`, `*.pyc`.
- Migration step: run `alembic upgrade head` as a separate init container or startup command before the API container starts receiving traffic.

---

## 14. Async Usage

### Rules

- All database operations must use `async`/`await` with `AsyncSession`.
- All I/O-bound operations (HTTP calls, file reads) must be async.
- Use `asyncpg` as the PostgreSQL async driver (`postgresql+asyncpg://...`).
- Never use `asyncio.run()` inside request handlers or FastAPI lifespan — the event loop is already running.
- Never use synchronous blocking calls in async functions (`time.sleep`, `requests.get`, blocking file I/O). Use `anyio.sleep`, `httpx.AsyncClient`, `aiofiles` respectively.
- CPU-bound work must be offloaded to `asyncio.run_in_executor()` with a thread or process pool.
- Use `asyncio.gather()` to run independent coroutines concurrently when appropriate.

```python
# Correct — concurrent DB fetches
user, order_count = await asyncio.gather(
    repo.get_by_id(user_id),
    order_repo.count_by_user(user_id),
)
```

---

## 15. Background Tasks

### When to Use

- Use FastAPI `BackgroundTasks` for lightweight, fire-and-forget work (send email, audit log).
- Use a proper task queue (ARQ with Redis, or Celery) for: retryable jobs, long-running tasks, scheduled jobs, tasks requiring persistence.

### FastAPI BackgroundTasks Pattern

```python
from fastapi import BackgroundTasks

@router.post("/users/{user_id}/welcome-email")
async def send_welcome(
    user_id: int,
    background_tasks: BackgroundTasks,
    db: DBSession,
) -> dict[str, str]:
    user = await UserService(db).get_by_id(user_id)
    background_tasks.add_task(send_email, email=user.email, template="welcome")
    return {"status": "queued"}
```

### Rules

- Background tasks must not share the request's DB session — they outlive the request. Create a new session inside the task.
- All background tasks must be idempotent — safe to run twice.
- Log task start and completion at `INFO` level.
- Errors in background tasks must be caught and logged — unhandled exceptions are silently dropped.

---

## 16. Retry-Safe & Idempotent Behavior

- All `POST` endpoints that create resources should accept a client-supplied `idempotency_key` header where appropriate and return the same response on duplicate requests.
- All database write operations must be safe to retry on transient failures.
- Use `ON CONFLICT DO NOTHING` / `ON CONFLICT DO UPDATE` in upsert patterns via SQLAlchemy `insert().on_conflict_do_nothing()`.
- Background tasks and Celery workers must be designed as idempotent operations.
- Startup code (migrations, seed data) must be safe to run on every deploy without side effects.
- HTTP `DELETE` must return `204` even if the resource was already deleted (idempotent by spec).

---

## 17. Security Defaults

- **CORS**: Default to restrictive. Only allow origins listed in `CORS_ORIGINS`. In production, never use `allow_origins=["*"]`.
- **HTTPS**: Enforce HTTPS at the load balancer or reverse proxy. The app itself does not terminate TLS.
- **Headers**: Use `slowapi` or middleware to add security headers (`X-Content-Type-Options`, `X-Frame-Options`, `Strict-Transport-Security`).
- **SQL injection**: Use SQLAlchemy ORM or `text()` with bound parameters only. Never format user input into SQL strings.
- **Password hashing**: Use `passlib[bcrypt]` with `CryptContext(schemes=["bcrypt"])`. Never use MD5, SHA1, or SHA256 for passwords.
- **Secrets**: Use `secrets.token_urlsafe(32)` to generate `SECRET_KEY` values.
- **File uploads**: Validate MIME type, enforce size limits, store outside the web root, never execute uploaded files.
- **Dependency versions**: Pin all dependencies in `pyproject.toml`. Run `pip-audit` or `safety` in CI.
- **Debug mode**: `DEBUG=false` and `DB_ECHO=false` in all non-local environments.
- **OpenAPI docs**: Disable in production (`docs_url=None, redoc_url=None`) or protect behind auth.

---

## 18. Performance & Scalability

- Use **connection pooling**: `pool_size=10`, `max_overflow=20` (tune per workload).
- Enable `pool_pre_ping=True` to detect stale connections.
- Use `expire_on_commit=False` in session factory to avoid lazy loads after commit.
- Use `selectinload` or `joinedload` for eager loading of relationships. Never rely on lazy loading in async context — it will raise `MissingGreenlet` errors.
- Paginate all list endpoints — never return unbounded query results.
- Add DB indexes on all columns used in `WHERE`, `ORDER BY`, and foreign keys.
- Use `EXPLAIN ANALYZE` in development to audit slow queries.
- Cache read-heavy, rarely-changing data with Redis (`aiocache` or `redis-py`).
- Use `uvicorn` with multiple workers behind a process manager (`gunicorn -k uvicorn.workers.UvicornWorker`) or deploy with horizontal scaling behind a load balancer.
- Set `--workers` to `(2 * CPU_COUNT) + 1` as a starting point.

---

## 19. Deployment Readiness Checklist

Before marking any feature or service ready for production, verify all of the following:

**Application**
- [ ] All environment variables documented in `.env.example`
- [ ] `DEBUG=false` and `DB_ECHO=false` set for production
- [ ] OpenAPI docs disabled or protected in production
- [ ] All secrets sourced from environment, not hardcoded
- [ ] `SECRET_KEY` is >= 32 characters and randomly generated

**Database**
- [ ] All migrations reviewed and applied (`alembic upgrade head`)
- [ ] All migrations have working `downgrade()` functions
- [ ] DB connection pooling configured
- [ ] Indexes exist for all FK and query columns

**API**
- [ ] `/health/live` and `/health/ready` endpoints working
- [ ] CORS configured with explicit allowed origins
- [ ] All auth-protected routes verified
- [ ] Pagination implemented on all list endpoints
- [ ] Error responses never expose stack traces

**Testing**
- [ ] Test coverage >= 80% on `app/`
- [ ] All integration tests pass against a real test database
- [ ] No tests depend on external services (mocked or containerized)

**Docker**
- [ ] Application runs as non-root user
- [ ] Image built and tested via `docker compose up --build`
- [ ] Health check passes in container
- [ ] No secrets in Dockerfile or committed compose files

**Observability**
- [ ] Structured JSON logging enabled for non-local environments
- [ ] Log level appropriate (`INFO` for production)
- [ ] No PII or secrets logged

**CI**
- [ ] `ruff` linting passes
- [ ] `mypy --strict` passes
- [ ] All tests pass
- [ ] `pip-audit` shows no critical vulnerabilities

---

## 20. Anti-Patterns to Avoid

| Anti-Pattern | Why | What to Do Instead |
|---|---|---|
| `from app.db.session import session` (module-level session) | Not thread/async safe | Always use `get_db` dependency via `Depends()` |
| `session.commit()` in a repository | Violates layer responsibility | Commit in the service layer only |
| Raw `os.getenv("KEY")` calls | Bypasses validation | Use `settings.KEY` from Pydantic Settings |
| `from app.models import *` | Namespace pollution | Explicit imports only |
| `async def f(): time.sleep(5)` | Blocks the event loop | Use `await asyncio.sleep(5)` |
| Lazy relationship loading in async | Raises `MissingGreenlet` | Use `selectinload()` / `joinedload()` |
| `SELECT *` ORM queries without joins | N+1 query problem | Use `selectinload` for relationships |
| `except Exception: pass` | Silences all errors | Log and re-raise, or handle specifically |
| Storing secrets in `.env` committed to git | Security breach | Use `.env.example` and inject secrets at runtime |
| Writing business logic in endpoint handlers | Untestable, unmaintainable | Move to service layer |
| Returning ORM objects from endpoints | Exposes DB structure, no validation | Always serialize via Pydantic `response_model` |
| `alembic revision --autogenerate` without review | May drop columns or skip changes | Always review and edit generated migrations |
| No input length limits | DoS / DB overflow | Always use `Field(max_length=...)` |
| Unbounded list queries | OOM, slow responses | Always paginate |
| `allow_origins=["*"]` in production | CORS bypass | Enumerate allowed origins explicitly |
| Using `datetime.utcnow()` | Deprecated, timezone-naive | Use `datetime.now(UTC)` |

---

## 21. Definition of Done

A task, feature, or bug fix is **Done** when all of the following are true:

1. **Code is typed**: all new functions and methods have complete type annotations; `mypy --strict` passes with no new errors.
2. **Tests written**: unit tests for all service methods; integration tests for all new/modified endpoints covering happy path and error cases.
3. **Tests pass**: `pytest` passes with no failures; coverage on changed files is >= 80%.
4. **Linting clean**: `ruff check .` and `ruff format --check .` pass with zero warnings.
5. **Migration included**: if DB schema changed, a reviewed Alembic migration file is committed with a working `downgrade()`.
6. **No secrets hardcoded**: no tokens, passwords, or keys appear in source code or committed config files.
7. **Documentation updated**: `.env.example` updated for new variables; README updated for new setup steps or changed behavior.
8. **Docker verified**: `docker compose up --build` starts without errors; health endpoints return `200`.
9. **Deployment checklist reviewed**: all applicable items in §19 confirmed.
10. **Code reviewed**: at least one peer review completed; reviewer has confirmed adherence to this SKILL.md.
