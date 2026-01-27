import json
from pydantic import BaseModel, ValidationError

from schemas.movie import Movie, MovieCreate, MovieUpdate, MovieUpdatePartial

# Файл для хранения данных
DATA_FILE = "movies.json"


# Хранилище данных о фильмах
class MovieStorage(BaseModel):
    slug_to_movie: dict[str, Movie] = {}

    # Сохранение данных в JSON файл
    def save_data(self):
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            f.write(self.model_dump_json(indent=4))

    """
    Возвращает список всех сохраненных объектов Movie.

    Возвращает:
        list[Movie]: список всех сохраненных объектов Movie
    """

    def get(self) -> list[Movie]:
        return list(self.slug_to_movie.values())

    """
    Возвращает объект Movie по его slug.

    Параметры:
        slug (str): slug объекта Movie

    Возвращает:
        Movie | None: объект Movie если найден, иначе None
    """

    def get_by_slug(self, slug: str) -> Movie | None:
        return self.slug_to_movie.get(slug)

    """
    Создает объект Movie на основе переданных параметров.

    Параметры:
        movie_create (MovieCreate): объект MovieCreate, содержащий параметры для создания Movie

    Возвращает:
        Movie: созданный объект Movie
    """

    def create(self, movie_create: MovieCreate) -> Movie:
        movie = Movie(
            **movie_create.model_dump(),
        )
        self.slug_to_movie[movie.slug] = movie
        self.save_data()
        return movie

    def update(
        self,
        movie: Movie,
        movie_in: MovieUpdate,
    ):
        for field_name, value in movie_in:
            setattr(movie, field_name, value)
        self.save_data()
        return movie

    def update_partial(
        self,
        movie: Movie,
        movie_in: MovieUpdatePartial,
    ):
        for field_name, value in movie_in.model_dump(exclude_unset=True).items():
            setattr(movie, field_name, value)
        self.save_data()
        return movie

    def delete_by_slug(self, slug: str) -> None:
        self.slug_to_movie.pop(slug, None)
        self.save_data()

    def delete(self, movie: Movie) -> None:
        self.delete_by_slug(slug=movie.slug)


# Загрузка данных из JSON файла
def load_storage() -> MovieStorage:
    try:
        # Пытаемся загрузить данные из файла
        return MovieStorage.model_validate_json(open(DATA_FILE, encoding="utf-8").read())
    except (FileNotFoundError, json.JSONDecodeError, ValidationError):
        # Если файл не найден или данные некорректны, создаем хранилище с данными по умолчанию
        storage = MovieStorage()
        storage.create(
            MovieCreate(
                slug="godfather",
                title="Крестный отец",
                description="Криминальная драма о семье мафиози Корлеоне",
                year=1972,
            )
        )
        storage.create(
            MovieCreate(
                slug="shawshank-redemption",
                title="Побег из Шоушенка",
                description="Драма о несправедливо осужденном банкире",
                year=1994,
            )
        )
        storage.create(
            MovieCreate(
                slug="dark-knight",
                title="Темный рыцарь",
                description="Бэтмен сражается с Джокером",
                year=2008,
            )
        )
        return storage


# Инициализация хранилища при запуске приложения
storage = load_storage()
