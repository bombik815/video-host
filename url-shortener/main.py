from fastapi import FastAPI, Request

app = FastAPI(
    title="URL Shortener",
    description="URL Shortener",
)


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
