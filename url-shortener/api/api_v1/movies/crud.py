import logging
from pydantic import BaseModel
from redis import Redis

from core import config
from schemas.movie import Movie, MovieCreate, MovieUpdate, MovieUpdatePartial

log = logging.getLogger(__name__)

redis = Redis(
    host=config.REDIS_HOST,
    port=config.REDIS_PORT,
    db=config.REDIS_DB_MOVIES,
    decode_responses=True,
)


# Хранилище данных о фильмах
class MovieStorage(BaseModel):
    slug_to_movie: dict[str, Movie] = {}

    def get(self) -> list[Movie]:
        # Получаем список фильмов from REDIS через hvals
        movies_json = redis.hvals(name=config.REDIS_MOVIES_HASH_NAME)
        return [Movie.model_validate_json(movie_json) for movie_json in movies_json]

    def get_by_slug(self, slug: str) -> Movie | None:
        # Получаем запись с REDIS по slug
        movie_json = redis.hget(name=config.REDIS_MOVIES_HASH_NAME, key=slug)
        if movie_json is None:
            return None
        return Movie.model_validate_json(movie_json)

    def _save_to_redis(self, movie: Movie) -> None:
        """Сохраняет информацию о фильме в Redis."""
        redis.hset(
            name=config.REDIS_MOVIES_HASH_NAME,
            key=movie.slug,
            value=movie.model_dump_json(),
        )

    def create(self, movie_create: MovieCreate) -> Movie:
        movie = Movie(
            **movie_create.model_dump(),
        )
        self._save_to_redis(movie)
        log.info("Created new movie: %s", movie.slug)
        return movie

    def update(
        self,
        movie: Movie,
        movie_in: MovieUpdate,
    ):
        for field_name, value in movie_in:
            setattr(movie, field_name, value)
        self._save_to_redis(movie)
        return movie

    def update_partial(
        self,
        movie: Movie,
        movie_in: MovieUpdatePartial,
    ):
        for field_name, value in movie_in.model_dump(exclude_unset=True).items():
            setattr(movie, field_name, value)
        self._save_to_redis(movie)
        return movie

    def _delete_from_redis(self, slug: str) -> None:
        """Удаляет информацию о фильме из Redis."""
        redis.hdel(config.REDIS_MOVIES_HASH_NAME, slug)

    def delete(self, movie: Movie) -> None:
        self._delete_from_redis(slug=movie.slug)
        log.info("The movies has been delete in storage.")

storage = MovieStorage()
