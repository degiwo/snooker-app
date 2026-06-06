# ADR 001: Repository Setup and Technology Stack

**Date**: 2026-06-06
**Status**: Accepted
**Authors**: Copilot CLI, Development Team

## Context

The snooker-app project requires a modern, scalable full-stack architecture supporting a web frontend and API backend. Key considerations include:

- Developer experience and productivity
- Type safety and code quality
- Testing and maintainability
- Deployment and containerization
- Long-term support and community maturity
- Performance and scalability

This decision record documents the chosen technology stack across frontend, backend, and DevOps/infrastructure layers, along with rationale for each choice and alternatives considered.

## Decision

The snooker-app repository adopts the following technology stack:

### Frontend Stack

| Category | Technology | Version | Rationale |
|----------|-----------|---------|-----------|
| **Framework** | Angular | 21.x | Modern, opinionated framework with excellent TypeScript support, built-in tooling, and strong dependency injection system |
| **Language** | TypeScript | 5.9+ | Strict type safety, superior DX, compile-time error detection |
| **Package Manager** | npm | 11.13+ | Stable, bundled with Node.js, excellent ecosystem support |
| **Testing** | Vitest | 4.0+ | Fast unit test runner with Vite integration, modern alternative to Jest |
| **Code Formatting** | Prettier | 3.8+ | Zero-config opinionated formatter, consistent style across codebase |
| **Build System** | Angular CLI | 21.x | Integrated build tooling, lazy loading support, AOT compilation by default |
| **Test Environment** | jsdom | 28.0+ | DOM simulation for unit tests without browser overhead |

**Angular-Specific Standards** (per copilot-instructions.md):
- Standalone components (default in Angular v20+)
- Signals for state management
- `input()` and `output()` functions (not decorators)
- Reactive forms over template-driven forms
- `ChangeDetectionStrategy.OnPush` for performance
- WCAG AA compliance with Axe accessibility checks
- `NgOptimizedImage` for static images

### Backend Stack

| Category | Technology | Version | Rationale |
|----------|-----------|---------|-----------|
| **Framework** | FastAPI | 0.136+ | Modern Python async framework with automatic API documentation, excellent performance, minimal boilerplate |
| **Language** | Python | 3.13+ | Latest stable release, focus on modern Python features, strong type hints support |
| **Package Manager** | uv | Latest | Fast, modern package manager written in Rust, superior to pip/Poetry in performance and DX |
| **Project Config** | pyproject.toml | PEP 518 | Modern Python packaging standard, single source of truth for dependencies and tools |
| **Testing** | pytest | 9.0+ | Industry standard, plugin-rich, excellent for async testing |
| **Code Quality** | ruff | 0.15+ | Fast linting and formatting in Rust, replaces pylint + black + isort |
| **Type Checking** | ty | Latest | Excellent Python type checker, faster than mypy, catches more errors |
| **Code Style** | Ruff formatter | 0.15+ | Enforced line length of 100 characters |

**Dependency Groups** (pyproject.toml):
- `dev`: Testing, linting, and type-checking tools

### Data Layer Stack

| Category | Technology | Rationale |
|----------|-----------|-----------|
| **Relational Database** | PostgreSQL 16 | Production-grade RDBMS with ACID compliance, excellent JSON/JSONB support, mature Python ecosystem (SQLAlchemy, asyncpg, etc.) |
| **Container Image** | postgres:16-alpine | Lightweight image (~160MB) for both development and production environments |
| **Data Persistence** | Docker named volumes | Persists across container restarts; managed by Docker; suitable for Hetzner SSH deployments |
| **Credential Management** | Environment variables (.env) | Secrets never committed to git; `.env.example` provides template; actual credentials stored on server only |

### DevOps & Infrastructure Stack

| Category | Technology | Rationale |
|----------|-----------|-----------|
| **Containerization** | Docker | Industry standard, reproducible builds, isolation |
| **Local Dev** | Docker Compose | Multi-container orchestration for local development matching production |
| **Container Registry** | GitHub Container Registry (GHCR) | Native GitHub integration, free for public images, no external vendor lock-in |
| **CI/CD** | GitHub Actions | Native GitHub integration, free for public repos, no separate login/secrets management |
| **Monorepo Structure** | apps/ directory pattern | Clear separation of concerns, independent versioning possible, shared workflows |
| **Build Automation** | Makefile | Simple, portable cross-platform task automation |

**CI/CD Pipelines**:
1. **Build and Push** (push trigger): Build Docker images for frontend and backend, push to GHCR
2. **CI** (push trigger): Code quality checks (linting, formatting, types, builds, tests)

**Local Development & Debugging**:

- Development docker-compose.yaml for local testing
- Production docker-compose.prod.yml for production-like environment

Local debugging (recommended):

- Backend
  - Docker Compose (recommended for parity):
    - docker-compose up backend
  - Run locally with auto-reload (fast edit/debug loop):
    - cd apps/backend
    - Install dependencies via the project's package manager (see pyproject.toml)
    - Run the server in reload mode: uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
  - Attach debugger (VSCode):
    - Existing config: `.vscode/launch.json` contains a "Python: Debug" entry targeting `apps/backend/app/main.py`.
    - Alternative: start FastAPI with debugpy and attach a remote debugger:
      - python -m debugpy --listen 5678 --wait-for-client -m uvicorn app.main:app --reload

- Frontend
  - Start dev server (live reload + source maps):
    - cd apps/frontend
    - npm install
    - npm run start (opens at http://localhost:4200)
  - Debugging in-browser / VSCode:
    - Use Chrome/Edge devtools for runtime inspection and breakpoints.
    - VSCode launch snippet to attach/launch browser (add to `.vscode/launch.json` if desired):
      {
        "name": "Attach to Chrome",
        "type": "pwa-chrome",
        "request": "launch",
        "url": "http://localhost:4200",
        "webRoot": "${workspaceFolder}/apps/frontend"
      }

Environment & tips
- Copy `.env.example` to `.env` and populate secrets before running Docker Compose or local servers.
- Prefer Docker Compose when the backend depends on other services (e.g., Postgres) to mirror production.
- Use direct runs for quick iterative debugging; use Docker Compose for end-to-end local integration testing.
## Future Considerations

### Potential Enhancements
1. **E2E Testing**: Add Playwright or Cypress for end-to-end testing
2. **API Documentation**: Leverage FastAPI's Swagger/OpenAPI for interactive API docs
3. **Database ORM**: Add SQLAlchemy ORM or async alternative when integrating database queries
4. **Database Migrations**: Implement Alembic for schema versioning (when ORM is selected)
5. **Authentication**: Implement OAuth2/JWT authentication (FastAPI has excellent support)
6. **Logging**: Add structured logging (python-json-logger, loguru)
7. **Monitoring**: Add application monitoring and tracing when production needs arise
8. **Kubernetes**: Migrate to K8s if scaling or multi-region deployment needed
9. **Containerization Improvements**: Add layer caching optimization, multi-stage builds

### Optional Tooling (Defer for Incremental Adoption)

The following tools are valuable additions but deferred to keep initial setup lightweight. They can be adopted incrementally as the project matures:

#### **Backend Security**

**Bandit** (PyCQA)
- **Purpose**: Security linter for Python, detects common security issues
- **Examples**: SQL injection risks, insecure randomness, hardcoded secrets
- **Why defer**: Security scanning less critical at MVP stage; add before production deployment
- **When to adopt**: When handling sensitive data or before first major release
- **Integration**: One-line addition to Makefile check target: `uv run bandit -r app/`

#### **Frontend Code Quality**

**ESLint** (OpenJS Foundation)
- **Purpose**: JavaScript/TypeScript linter, catches code quality issues and bugs
- **Examples**: Unused variables, unreachable code, incorrect async/await usage
- **Why defer**: Angular's strict TypeScript config + Prettier already catches most issues; ruff equivalent exists via Prettier plugins
- **When to adopt**: As codebase grows or when team needs stricter standards
- **Integration**: `npm install --save-dev eslint @typescript-eslint/parser @typescript-eslint/eslint-plugin`
- **Config**: Add `.eslintrc.json` with Angular-specific rules

#### **Git Hooks Automation**

**husky** + **lint-staged** (Conventional Commits community)
- **Purpose**: Pre-commit hooks to enforce code quality before pushing
- **Examples**: Auto-format, lint, test before commit
- **Why defer**: Makefile targets sufficient; can be enforced in CI/CD
- **When to adopt**: When team size grows and more guardrails needed
- **Integration**: `npm install husky lint-staged --save-dev` + `.husky/pre-commit` config

#### **Dependency Security Scanning**

**pip-audit** (PyPA)
- **Purpose**: Audit Python dependencies for known security vulnerabilities
- **Examples**: Detect outdated packages with CVEs
- **Why defer**: GitHub Dependabot already monitors PyPI for security; can add for explicit audits
- **When to adopt**: When handling high-security applications
- **Integration**: `uv run pip-audit`

#### **Backend Error Tracking & Monitoring**

**Sentry** (Sentry Inc.)
- **Purpose**: Real-time error tracking, performance monitoring, and crash reporting
- **Examples**: Catch unhandled exceptions, track error trends, identify performance bottlenecks
- **Why defer**: Additional overhead and external dependency; local logging sufficient for MVP
- **When to adopt**: Before production deployment or when running in distributed environment
- **Integration**: `pip install sentry-sdk` + initialize in `main.py` with DSN
- **Note**: Free tier includes limited error events; consider cost at scale

#### **Backend Rate Limiting**

**slowapi** (Lauren Vintage)
- **Purpose**: Rate limiting middleware for FastAPI, protect API from abuse and DDoS
- **Examples**: Limit requests per IP, per user, or per endpoint
- **Why defer**: Not needed for MVP without public API; internal usage doesn't require protection
- **When to adopt**: When API becomes public or exposed to untrusted users
- **Integration**: `pip install slowapi` + add decorators to endpoints: `@limiter.limit("100/minute")`
- **Alternative**: Native FastAPI middleware with Redis for distributed rate limiting

#### **OpenAPI Client Generation**

**openapi-generator** (OpenAPI Generator Community)
- **Purpose**: Auto-generate client SDKs, server stubs from OpenAPI/Swagger specifications
- **Examples**: Generate TypeScript client from FastAPI OpenAPI spec, generate server boilerplate
- **Why defer**: FastAPI auto-generates OpenAPI spec; manual client code sufficient for single frontend
- **When to adopt**: When building multiple clients (web, mobile, desktop) or SDKs for third parties
- **Integration**: `npm install @openapitools/openapi-generator-cli` + configure generator config
- **Benefit**: Keeps client/server contracts in sync automatically

#### **Database Migrations**

**Alembic** (SQLAlchemy Project)
- **Purpose**: Database migration tool, manage schema changes across versions
- **Examples**: Track column additions, renames, constraint changes in version control
- **Why defer**: No ORM layer yet; will be implemented alongside ORM selection (see ADR-002)
- **When to adopt**: Immediately when adding SQLAlchemy ORM
- **Integration**: `pip install alembic` + `alembic init migrations` + create migration scripts
- **Note**: Industry standard for Python database migrations; pairs perfectly with SQLAlchemy

#### **API Load Testing**

**locust** (HeadlessBrowser/Locust Project)
- **Purpose**: Load testing framework, simulate concurrent users and measure performance
- **Examples**: Test API under 1000 concurrent users, identify bottlenecks
- **Why defer**: Performance testing not critical at MVP; local testing sufficient
- **When to adopt**: Before scaling to production or when handling high-traffic scenarios
- **Integration**: `pip install locust` + create `locustfile.py` with test scenarios
- **Benefit**: Write tests in Python, easily integrates with FastAPI

#### **Environment Configuration**

**pydantic-settings** (Pydantic Project)
- **Purpose**: Structured environment variable validation and management
- **Examples**: Load config from .env files, validate types, provide defaults
- **Why defer**: Simple environment variables sufficient for MVP
- **When to adopt**: As configuration grows complex or when multiple environments (dev/staging/prod)
- **Integration**: `pip install pydantic-settings` + create `settings.py` with ConfigModel
- **Note**: Better than python-dotenv; integrates with Pydantic's validation

#### **Caching Layer**

**Redis** (Redis Labs) + **aioredis** or **FastAPI-Cache2**
- **Purpose**: In-memory caching to reduce database queries and API calls
- **Examples**: Cache API responses, cache database query results
- **Why defer**: Premature optimization; unnecessary at MVP scale
- **When to adopt**: When response times degrade or database becomes bottleneck
- **Integration**: `docker-compose.yaml` Redis service + `pip install aioredis` + cache decorators
- **Note**: Requires operational consideration (persistence, memory management)

#### **Background Task Queue**

**Celery** (Celery Project) + RabbitMQ/Redis
- **Purpose**: Distributed task queue for long-running or periodic tasks
- **Examples**: Send emails asynchronously, generate reports, scheduled cleanup jobs
- **Why defer**: Synchronous processing adequate for MVP; adds architectural complexity
- **When to adopt**: When needing async job processing (emails, heavy computations)
- **Integration**: `pip install celery redis` + define tasks, add beat scheduler for cron jobs
- **Alternative**: Simpler approach with FastAPI background tasks (not persistent)

#### **Frontend Analytics**

**Mixpanel** / **Google Analytics** / **Plausible Analytics**
- **Purpose**: Track user behavior, page views, conversion funnels
- **Examples**: Understand user journey, identify drop-off points
- **Why defer**: User tracking not critical for MVP; privacy concerns; GDPR compliance needed
- **When to adopt**: When product is public and understanding user behavior is important
- **Integration**: Varies by provider; usually simple script tag + event tracking code
- **Note**: Consider privacy laws (GDPR, CCPA) before implementation

#### **Frontend Performance Monitoring**

**web-vitals** (Google)
- **Purpose**: Measure Core Web Vitals (LCP, FID, CLS) to understand real user experience
- **Examples**: Track page load time, input responsiveness, visual stability
- **Why defer**: Performance optimization premature at MVP; good foundation already set
- **When to adopt**: When performance becomes noticeable issue or SEO becomes priority
- **Integration**: `npm install web-vitals` + send metrics to analytics service
- **Benefit**: Lightweight library, helps identify performance problems early

### Rationale for Deferring Optional Tooling

✅ **Incremental adoption** keeps setup lean and onboarding smooth  
✅ **Baseline is sufficient** - Current stack already has strong type checking, formatting, and testing  
✅ **Avoid tool fatigue** - Too many tools create maintenance burden and slow down developers  
✅ **Add when needed** - Adopt tools when specific pain points emerge (security, accessibility, etc.)  
✅ **Easy to integrate** - All listed tools integrate cleanly with current setup; no breaking changes needed later  

### Technology Debt Monitoring
- Monitor **ruff** and **uv** adoption in broader ecosystem
- Watch **Biome** maturity; evaluate for future frontend setup
- Keep Angular upgrade path clear (stay on latest LTS versions)
- Periodically review FastAPI alternatives as ecosystem evolves
- Track PostgreSQL ecosystem evolution; evaluate connection pooling solutions (pgBouncer, asyncpg)
- Monitor ORM ecosystem for async-first alternatives to SQLAlchemy
