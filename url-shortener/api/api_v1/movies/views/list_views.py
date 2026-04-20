from fastapi import (
    status,
    APIRouter,
    Depends,
    HTTPException,
)

from api.api_v1.movies.crud import storage
from api.api_v1.movies.dependencies import (
    api_token_or_user_basic_auth_required_for_unsafe_methods,
)

from schemas.movie import Movie, MovieCreate, MovieRead

router = APIRouter(
    prefix="/movies",
    tags=["Movies"],
    dependencies=[
        # Depends(api_token_required_for_unsafe_methods),
        Depends(api_token_or_user_basic_auth_required_for_unsafe_methods),
    ],
    responses={
        status.HTTP_401_UNAUTHORIZED: {
            "description": "Unauthenticated. Only for unsafe method.",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "Invalid API token",
                    },
                },
            },
        },
    },
)

"""
Возвращает список фильмов

Возвращает:
    list[Movie]: список объектов фильмов

"""


@router.get("/", response_model=list[MovieRead])
def get_movies() -> list[Movie]:
    return storage.get()


@router.post("/", response_model=Movie, status_code=status.HTTP_201_CREATED)
def create_movie(movie_create: MovieCreate):
    # Проверим если такая запись в БД уже существует, тогда выдаем ошибку 409
    if not storage.get_by_slug(movie_create.slug):
        return storage.create(movie_create)
    raise HTTPException(
        status_code=status.HTTP_409_CONFLICT,
        detail=f"Movie URL with slug {movie_create.slug} already exists.",
    )
