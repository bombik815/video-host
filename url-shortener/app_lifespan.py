from contextlib import asynccontextmanager

from fastapi import FastAPI

from api.api_v1.short_urls.crud import storage as short_urls_storage
from api.api_v1.movies.crud import storage as movies_storage


@asynccontextmanager
async def lifespan(app: FastAPI):
    short_urls_storage.init_storage_from_state()
    movies_storage.init_storage_from_state()
    yield
