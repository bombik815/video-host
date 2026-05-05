# FastAPI URL Shortener

## Develop

### Setup

Mark `url-shortener` as `Sources Root` in your IDE.

### Run
### Configure pre-commit
Install pre-commit hook:
```shell
pre-commit install
```


Go to the working directory:

```shell
cd url-shortener
```

Run the dev server:

```shell
fastapi dev
```

Or run Uvicorn directly:

```shell
uvicorn main:app --host 127.0.0.1 --port 8080
```

### Ruff

Check the project:

```shell
ruff check .
```

Apply safe fixes:

```shell
ruff check . --fix
```

Apply unsafe fixes too:

```shell
ruff check . --fix --unsafe-fixes
```

Use `--unsafe-fixes` only when you have reviewed the proposed changes.

Run the formatter check:

```shell
ruff format . --check
```

Format files:

```shell
ruff format .
```

## Project Structure

```text
url-shortener/
|-- main.py
|-- api/
|   |-- __init__.py
|   |-- redirect_views.py
|   `-- api_v1/
|       |-- __init__.py
|       `-- short_urls/
|           |-- crud.py
|           |-- dependencies.py
|           `-- views/
|               |-- list_views.py
|               `-- details_views.py
`-- schemas/
    `-- short_url.py
```

## Snippets

Generate token:

```shell
python -c "import secrets; print(secrets.token_urlsafe(16))"
```

## Redis Commands

Useful commands for this project:

```shell
# Check Redis connection
docker exec -it redis redis-cli PING

# ===== TOKENS: Redis DB 1, set "tokens" =====
docker exec -it redis redis-cli -n 1 SADD tokens my-secret-token
docker exec -it redis redis-cli -n 1 SMEMBERS tokens
docker exec -it redis redis-cli -n 1 SISMEMBER tokens my-secret-token
docker exec -it redis redis-cli -n 1 SREM tokens my-secret-token
docker exec -it redis redis-cli -n 1 SCARD tokens
docker exec -it redis redis-cli -n 1 TYPE tokens

# ===== BASIC AUTH USERS: Redis DB 2 =====
docker exec -it redis redis-cli -n 2 SET alice alice123
docker exec -it redis redis-cli -n 2 SET john john456
docker exec -it redis redis-cli -n 2 GET alice
docker exec -it redis redis-cli -n 2 EXISTS alice
docker exec -it redis redis-cli -n 2 KEYS '*'
docker exec -it redis redis-cli -n 2 DEL alice

# ===== SHORT URLS: Redis DB 3 =====
docker exec -it redis redis-cli -n 3 KEYS '*'
docker exec -it redis redis-cli -n 3 DBSIZE

# ===== COMMON USEFUL COMMANDS =====
docker exec -it redis redis-cli INFO
docker exec -it redis redis-cli -n 1 DBSIZE
docker exec -it redis redis-cli -n 2 DBSIZE
docker exec -it redis redis-cli -n 3 DBSIZE
```

## CLI Commands

Run management commands:

```shell
uv run --script url-shortener/manage.py [command]
```

Examples:

```shell
uv run --script url-shortener/manage.py token check my-secret-token
uv run --script url-shortener/manage.py token create
uv run --script url-shortener/manage.py token add my-secret-token
uv run --script url-shortener/manage.py token list
uv run --script url-shortener/manage.py token remove my-secret-token
```
