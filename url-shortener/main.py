import logging

import uvicorn
from fastapi import FastAPI
from fastapi import Request
from app_lifespan import lifespan

from api import router as api_router

from api.redirect_views import router as redirect_views
from core.config import LOG_FORMAT, LOG_LEVEL

logging.basicConfig(
    level=LOG_LEVEL,
    format=LOG_FORMAT
)
app = FastAPI(
    title="URL Shortener",
    lifespan=lifespan,
    description="URL Shortener",

)


app.include_router(redirect_views)
app.include_router(api_router)


@app.get("/")
async def read_root(
    request: Request,
    name: str = "Shortener",
):
    """
    Корневой view - возвращает JSON со ссылками на документацию
    """
    docs_url = request.url.replace(
        path="/docs",
        query="",
    )
    redoc_url = request.url.replace(
        path="/redoc",
        query="",
    )

    return {
        "message": f"Welcome to the URL {name} API",
        "docs": str(docs_url),
        "redoc": str(redoc_url),
    }


if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=8080)