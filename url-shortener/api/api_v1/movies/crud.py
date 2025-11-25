from pydantic import BaseModel

from schemas.movie import Movie, MovieCreate


class MovieStorage(BaseModel):
    slug_to_movie: dict[str, Movie] = {}

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
        return movie

    def delete_by_slug(self, slug: str) -> None:
        self.slug_to_movie.pop(slug, None)

    def delete(self, movie: Movie) -> None:
        self.delete_by_slug(slug=movie.slug)


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
