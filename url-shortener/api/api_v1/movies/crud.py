import logging
from pydantic import BaseModel, ValidationError
from redis import Redis

from core import config
from core.config import MOVIES_STORAGE_FILEPATH
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

    # Сохраняет текущее состояние хранилища в JSON-файл.
    def save_state(self) -> None:
        MOVIES_STORAGE_FILEPATH.write_text(
            self.model_dump_json(indent=2),
            encoding="utf-8",
        )
        log.info("Saved movies state to storage file.")

    # Загружает состояние хранилища из JSON-файла.
    @classmethod
    def from_state(cls) -> "MovieStorage":
        if not MOVIES_STORAGE_FILEPATH.exists():
            log.info("Movies storage file does not exist.")
            return MovieStorage()
        return cls.model_validate_json(
            MOVIES_STORAGE_FILEPATH.read_text(encoding="utf-8")
        )

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
        redis.hdel(name=config.REDIS_MOVIES_HASH_NAME, key=slug)

    def delete_by_slug(self, slug: str) -> None:
        self.slug_to_movie.pop(slug, None)
        self._delete_from_redis(slug)
        self.save_state()
        log.info("The movies has been delete in storage.")

    def delete(self, movie: Movie) -> None:
        self.delete_by_slug(slug=movie.slug)
        log.info("The movies has been delete in storage.")

    def init_storage_from_state(self) -> None:
        """
        Инициализирует хранилище из файла состояния.
        Пытается загрузить данные из файла. В случае ошибки валидации,
        перезаписывает файл текущим состоянием хранилища.
        """
        try:
            data = MovieStorage().from_state()
        except ValidationError:
            self.save_state()
            log.warning("Rewritten movies storage file due to validation error.")
            return

        self.slug_to_movie.update(
            data.slug_to_movie,
        )
        log.warning("Recovered movie data from storage file.")


storage = MovieStorage()
