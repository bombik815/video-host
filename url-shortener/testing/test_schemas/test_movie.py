from unittest import TestCase

from schemas.movie import Movie, MovieCreate, MovieUpdate, MovieUpdatePartial


class MovieCreateTestCase(TestCase):
    def test_movie_can_be_created_from_create_schema(self) -> None:
        movie_in = MovieCreate(
            title="title",
            slug="some-slug",
            description="some-description",
            year=1999,
        )

        movie = Movie(**movie_in.model_dump())
        self.assertEqual(movie_in.title, movie.title)
        self.assertEqual(movie_in.slug, movie.slug)
        self.assertEqual(movie_in.description, movie.description)
        self.assertEqual(movie_in.year, movie.year)
        self.assertEqual("", movie.notes)
        self.assertEqual("draft", movie.status)
        self.assertEqual(0, movie.view_count)

    def test_movie_create_accepts_different_payloads(self) -> None:
        # Проверяем создание фильма из нескольких валидных наборов данных.
        cases = [
            {
                "title": "The Matrix",
                "slug": "the-matrix",
                "description": "",
                "year": 1999,
            },
            {
                "title": "Arrival",
                "slug": "arrival-2016",
                "description": "First contact drama with nonlinear storytelling.",
                "year": 2016,
            },
            {
                "title": "Blade Runner 2049",
                "slug": "blade-runner-2049",
                "description": "d" * 200,
                "year": 2017,
            },
        ]

        for payload in cases:
            with self.subTest(slug=payload["slug"], year=payload["year"]):
                movie_in = MovieCreate(**payload)
                movie = Movie(**movie_in.model_dump())

                self.assertEqual(payload["title"], movie.title)
                self.assertEqual(payload["slug"], movie.slug)
                self.assertEqual(payload["description"], movie.description)
                self.assertEqual(payload["year"], movie.year)
                self.assertEqual("", movie.notes)
                self.assertEqual("draft", movie.status)
                self.assertEqual(0, movie.view_count)

    def test_movie_description_is_preserved_for_valid_lengths(self) -> None:
        # Проверяем, что допустимая длина описания сохраняется без изменений.
        descriptions = [
            "",
            "Short description",
            "x" * 200,
        ]

        for description in descriptions:
            with self.subTest(description_length=len(description)):
                movie_in = MovieCreate(
                    title="Interstellar",
                    slug=f"interstellar-{len(description)}",
                    description=description,
                    year=2014,
                )
                movie = Movie(**movie_in.model_dump())

                self.assertEqual(description, movie.description)
                self.assertLessEqual(len(movie.description), 200)


class MovieUpdateTestCase(TestCase):
    def test_movie_description_can_be_updated_from_update_schema(self) -> None:
        movie_in = Movie(
            title="old-title",
            slug="some-slug",
            description="old-description",
            year=1999,
            notes="internal-note",
            status="published",
            view_count=123,
        )
        movie_update = MovieUpdate(
            title=movie_in.title,
            description="new-description",
            year=movie_in.year,
        )

        updated_movie = movie_in.model_copy(
            update=movie_update.model_dump(include={"description"}),
        )

        self.assertEqual(movie_update.description, updated_movie.description)
        self.assertEqual(movie_in.title, updated_movie.title)
        self.assertEqual(movie_in.year, updated_movie.year)
        self.assertEqual(movie_in.slug, updated_movie.slug)
        self.assertEqual(movie_in.notes, updated_movie.notes)
        self.assertEqual(movie_in.status, updated_movie.status)
        self.assertEqual(movie_in.view_count, updated_movie.view_count)


class MoviePartialUpdateTestCase(TestCase):
    def test_empty_partial_update_does_not_change_movie(self) -> None:
        movie_in = Movie(
            title="old-title",
            slug="some-slug",
            description="old-description",
            year=1999,
            notes="internal-note",
            status="published",
            view_count=123,
        )
        movie_update = MovieUpdatePartial()

        updated_movie = movie_in.model_copy(
            update=movie_update.model_dump(exclude_none=True),
        )

        self.assertEqual(movie_in, updated_movie)

    def test_partial_update_changes_only_provided_fields(self) -> None:
        movie_in = Movie(
            title="old-title",
            slug="some-slug",
            description="old-description",
            year=1999,
            notes="internal-note",
            status="published",
            view_count=123,
        )
        movie_update = MovieUpdatePartial(description="new-description")

        updated_movie = movie_in.model_copy(
            update=movie_update.model_dump(exclude_none=True),
        )

        self.assertEqual(movie_update.description, updated_movie.description)
        self.assertEqual(movie_in.title, updated_movie.title)
        self.assertEqual(movie_in.year, updated_movie.year)
        self.assertEqual(movie_in.slug, updated_movie.slug)
        self.assertEqual(movie_in.notes, updated_movie.notes)
        self.assertEqual(movie_in.status, updated_movie.status)
        self.assertEqual(movie_in.view_count, updated_movie.view_count)
