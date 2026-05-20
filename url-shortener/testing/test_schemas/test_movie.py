from unittest import TestCase

from schemas.movie import Movie, MovieCreate, MovieUpdate


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
