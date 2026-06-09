from typing import ClassVar
from unittest import TestCase

from api.api_v1.movies.crud import storage
from schemas.movie import (
    Movie,
    MovieCreate,
    MovieUpdate,
    MovieUpdatePartial,
)
from testing import ensure_testing_environment

ensure_testing_environment()


def create_movie() -> Movie:
    """Создаёт и возвращает Фильм для тестов."""

    create_movie_in = MovieCreate(
        title="Some title",
        description="Some description",
        year=2005,
        slug="some-slug",
    )
    return storage.create(create_movie_in)


class MovieStorageUpdateTestCase(TestCase):
    def setUp(self) -> None:
        """Создаёт тестовый Фильм перед каждым тестом."""
        self.movie = create_movie()

    def tearDown(self) -> None:
        """Удаляет тестовый Фильм после каждого теста."""
        storage.delete(self.movie)

    def test_update(self) -> None:
        """Проверяет полное обновление описания фильма."""
        movie_update = MovieUpdate(**self.movie.model_dump())
        old_description = self.movie.description
        movie_update.description *= 2

        updated_movie = storage.update(
            movie=self.movie,
            movie_in=movie_update,
        )

        self.assertNotEqual(
            old_description,
            updated_movie.description,
        )
        self.assertEqual(
            movie_update,
            MovieUpdate(**updated_movie.model_dump()),
        )

    def test_update_partial(self) -> None:
        """Проверяет частичное обновление описания фильма."""
        movie_partial_update = MovieUpdatePartial(
            description=self.movie.description * 2,
        )
        old_description = self.movie.description
        old_title = self.movie.title
        old_year = self.movie.year
        old_slug = self.movie.slug

        updated_movie = storage.update_partial(
            movie=self.movie,
            movie_in=movie_partial_update,
        )

        self.assertNotEqual(
            old_description,
            updated_movie.description,
        )
        self.assertEqual(
            movie_partial_update.description,
            updated_movie.description,
        )
        self.assertEqual(old_title, updated_movie.title)
        self.assertEqual(old_year, updated_movie.year)
        self.assertEqual(old_slug, updated_movie.slug)


class MovieStorageGetMoviesTestCase(TestCase):

    MOVIES_COUNT = 3
    movies: ClassVar[list[Movie]] = []

    @classmethod
    def setUpClass(cls) -> None:
        cls.movies = [create_movie() for _ in range(cls.MOVIES_COUNT)]

    @classmethod
    def tearDownClass(cls) -> None:
        for movie in cls.movies:
            storage.delete(movie)

    def test_get_list(self) -> None:
        movies = storage.get()
        expected_movies = {mv.slug for mv in self.movies}
        slugs = {mv.slug for mv in movies}

        self.assertEqual(expected_movies, slugs)

    def test_get_by_slug(self) -> None:
        for movie in self.movies:
            with self.subTest(
                slug=movie.slug,
                msg=f"Validate can slug {movie.slug!r}",
            ):
                db_short_url = storage.get_by_slug(movie.slug)
                self.assertEqual(movie, db_short_url)
