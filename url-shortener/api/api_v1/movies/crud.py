import logging
from pydantic import BaseModel, ValidationError

from core.config import MOVIES_STORAGE_FILEPATH
from schemas.movie import Movie, MovieCreate, MovieUpdate, MovieUpdatePartial

log = logging.getLogger(__name__)


# Хранилище данных о фильмах
class MovieStorage(BaseModel):
    slug_to_movie: dict[str, Movie] = {}

    # Сохраняет текущее состояние хранилища в JSON-файл.
    def save_state(self) -> None:
        MOVIES_STORAGE_FILEPATH.write_text(self.model_dump_json(indent=2))
        log.info("Saved movies state to storage file.")

    # Загружает состояние хранилища из JSON-файла.
    @classmethod
    def from_state(cls) -> "MovieStorage":
        if not MOVIES_STORAGE_FILEPATH.exists():
            log.info("Movies storage file does not exist.")
            return MovieStorage()
        return cls.model_validate_json(MOVIES_STORAGE_FILEPATH.read_text())

    def get(self) -> list[Movie]:
        return list(self.slug_to_movie.values())

    def get_by_slug(self, slug: str) -> Movie | None:
        return self.slug_to_movie.get(slug)

    def create(self, movie_create: MovieCreate) -> Movie:
        movie = Movie(
            **movie_create.model_dump(),
        )
        self.slug_to_movie[movie.slug] = movie
        log.info("Created new movie: %s", movie.slug)
        self.save_state()  # Сохраняем состояние после изменения
        return movie

    def update(
        self,
        movie: Movie,
        movie_in: MovieUpdate,
    ):
        for field_name, value in movie_in:
            setattr(movie, field_name, value)
        self.save_state()
        return movie

    def update_partial(
        self,
        movie: Movie,
        movie_in: MovieUpdatePartial,
    ):
        for field_name, value in movie_in.model_dump(exclude_unset=True).items():
            setattr(movie, field_name, value)
        self.save_state()
        return movie

    def delete_by_slug(self, slug: str) -> None:
        self.slug_to_movie.pop(slug, None)
        self.save_state()

    def delete(self, movie: Movie) -> None:
        self.delete_by_slug(slug=movie.slug)


# При запуске приложения пытаемся загрузить хранилище из файла.
# Если не получается (файл не найден, поврежден или пуст), создаем новое хранилище.
try:
    storage = MovieStorage().from_state()
    log.warning("Recovered data from storage file.")
except ValidationError:
    storage = MovieStorage()
    storage.save_state()
    log.warning("Rewritten storage file due to validation error.")
