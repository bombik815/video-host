# FastAPI URL  Shortener

## Develop:

### Setup:

Right click `url-shortener` -> Mark directory as -> `Sources Root`



### Run:

Go to work directory:
```shell
cd url-shortener
```

Run dev server:
```shell
fastapi dev
```
```shell
uvicorn main:app --host 127.0.0.1 --port 8080
```

```shell
url-shortener/
├── main.py              # Основной FastAPI-приложение
├── api/                 # Роутеры API
│   ├── __init__.py      # Объединяет v1 API
│   ├── redirect_views.py # Роутер для редиректов (/r/{slug})
│   └── api_v1/          # Версия v1 API
│       ├── __init__.py  # Объединяет подмодули
│       └── short_urls/  # Управление короткими URL
│           ├── crud.py  # Логика хранения
│           ├── dependencies.py # Зависимости для валидации
│           └── views/   # Эндпоинты API
│               ├── list_views.py    # Список URL
│               └── details_views.py # Подробности/удаление
└── schemas/             # Pydantic-модели
    └── short_url.py     # Определение моделей
```

## Snippets
```shell
python -c "import secrets; print(secrets.token_urlsafe(16))"
```
### Пример команды для REDIS 
```
# ===== ДОБАВЛЕНИЕ ПОЛЬЗОВАТЕЛЕЙ =====
docker exec -it redis redis-cli -n 2 SET alice alice123
docker exec -it redis redis-cli -n 2 SET john john456
docker exec -it redis redis-cli -n 2 SET maria maria789

# ===== ПОЛУЧЕНИЕ ДАННЫХ =====
docker exec -it redis redis-cli -n 2 GET alice 
docker exec -it redis redis-cli -n 2 GETALL john

# ===== ПРОВЕРКА СУЩЕСТВОВАНИЯ =====
docker exec -it redis redis-cli -n 2 EXISTS alice

# ===== СПИСОК ВСЕХ ПОЛЬЗОВАТЕЛЕЙ =====
docker exec -it redis redis-cli -n 2 KEYS users:*

# ===== УДАЛЕНИЕ ПОЛЬЗОВАТЕЛЯ =====
docker exec -it redis redis-cli -n 2 DEL alice


# Добавляем первый токен в множество с ключом 'tokens'
SADD tokens f8I7ZdAF0p_CYdVQQZ6Fqg

# Добавляем второй токен в то же множество
SADD tokens another_token_string_abc123

# Теперь SMEMBERS сработает и вернет все токены из множества
SMEMBERS tokens
```
