from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from movies.models import AgeRating, Country, Language, Movie, Studio


class CoreViewsTests(TestCase):
    def setUp(self):
        country = Country.objects.create(name="SmokeCountry", code="SC")
        lang = Language.objects.create(name="SmokeLang", code="sl")
        age = AgeRating.objects.create(code="13+", description="smoke")
        studio = Studio.objects.create(name="SmokeStudio", country=country)
        self.movie = Movie.objects.create(
            title="Smoke Film",
            synopsis="smoke",
            release_year=2024,
            duration_minutes=98,
            age_rating=age,
            studio=studio,
            country=country,
            language=lang,
            is_featured=True,
        )
        self.user = User.objects.create_user(username="smokeuser", password="Pass12345!")

    def test_home_page(self):
        response = self.client.get(reverse("core:home"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'id="wrapper"')

    def test_movies_list_page(self):
        response = self.client.get(reverse("movies:list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'id="movie-filter-form"')

    def test_movie_detail_actions_for_authenticated_user(self):
        self.client.login(username="smokeuser", password="Pass12345!")
        response = self.client.get(reverse("movies:detail", kwargs={"slug": self.movie.slug}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "data-favorite-toggle")
