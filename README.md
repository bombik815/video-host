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
