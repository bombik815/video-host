---
name: fastapi-test-coverage
description: Run unit tests with coverage on FastAPI+Redis projects. Handles env vars, Redis port conflicts, and .coveragerc setup. Use when the user wants to run tests, generate coverage reports, or troubleshoot test failures related to environment configuration.
---

# SKILL: Run Tests with Coverage (FastAPI + Redis)

> For FastAPI projects backed by Redis where tests require specific env vars
> and a dedicated test Redis instance on a separate port.

---

## Quick Start

Run tests with coverage in one command:

```shell
$env:TESTING=1; $env:REDIS_PORT=6380; python -m coverage run -m unittest
```

Then view results:

```shell
python -m coverage report
python -m coverage html   # if .coveragerc configured
```

---

## Why This Skill Exists

Running `coverage run -m unittest` on a FastAPI+Redis project typically fails 3 times before working:

1. `coverage` is installed but not in PATH → must use `python -m coverage`
2. Tests fail without `TESTING=1` env var (app expects it to switch config)
3. Tests connect to the wrong Redis port (prod port 6379 vs test port 6380)

This skill eliminates that debugging cycle.

---

## Step-by-Step Procedure

### 1. Check Prerequisites

```shell
# Verify coverage is installed (may not be in PATH)
pip show coverage 2>$null; python -m coverage --version 2>$null

# Verify test Redis is running
docker ps | Select-String "redis"
```

### 2. Discover Redis Test Port

The project's `docker-compose.yml` typically defines a test Redis on a different port than production.

```shell
# Check which Redis ports are open
Test-NetConnection -ComputerName localhost -Port 6379 -WarningAction SilentlyContinue | Select-Object TcpTestSucceeded
Test-NetConnection -ComputerName localhost -Port 6380 -WarningAction SilentlyContinue | Select-Object TcpTestSucceeded
```

Read `core/config.py` or `docker-compose*.yml` to confirm the test Redis port.
Common pattern: production on **6379**, tests on **6380**.

### 3. Set Environment and Run

```shell
# PowerShell (one-liner)
$env:TESTING=1; $env:REDIS_PORT=6380; python -m coverage run -m unittest

# If TESTING env var name differs, check core/config.py for the expected variable name
```

### 4. Generate Reports

```shell
# Summary table
python -m coverage report

# HTML report (requires .coveragerc)
python -m coverage html
```

### 5. Create .coveragerc (if missing)

```ini
[html]
directory = codecov
```

Place in the project root (next to `pyproject.toml`).

---

## Common Gotchas

| Problem | Cause | Fix |
|---------|-------|-----|
| `'coverage' is not recognized` | Not in PATH | Use `python -m coverage` instead |
| `ConnectionRefusedError` on Redis | Wrong port or Redis not running | Check `docker ps`, set `$env:REDIS_PORT` |
| Tests fail with config errors | `TESTING=1` not set | Set `$env:TESTING=1` before running |
| `ModuleNotFoundError: testing` | Tests import internal modules | Run from project root, not `url-shortener/` |
| Coverage shows 0% | Running from wrong directory | Run from the directory containing the app package |

---

## Integration with Existing Skills

This skill complements `fastapi-backend` (section 11 — Testing Standards).
Use `fastapi-backend` for writing tests; use this skill for running them with coverage.

---

## Stopping Condition

Stop when:
- `python -m coverage report` shows results with non-zero percentages
- OR the user confirms tests pass and coverage is generated
