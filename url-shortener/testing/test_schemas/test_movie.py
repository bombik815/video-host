from unittest import TestCase

from schemas.movie import Movie, MovieCreate


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
        self.assertEqual(movie.slug, movie.slug)
        self.assertEqual(movie.description, movie.description)
        self.assertEqual(movie.year, movie.year)
