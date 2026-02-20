from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from movies.models import AgeRating, Country, Language, Movie, Studio
from reviews.models import Review


class ModelsTests(TestCase):
    def setUp(self):
        self.country = Country.objects.create(name="TestCountry", code="TC")
        self.lang = Language.objects.create(name="TestLang", code="tl")
        self.age = AgeRating.objects.create(code="12+", description="test")
        self.studio = Studio.objects.create(name="Studio", country=self.country)

    def test_movie_slug_generated(self):
        movie = Movie.objects.create(
            title="My Film",
            synopsis="x",
            release_year=2024,
            duration_minutes=100,
            age_rating=self.age,
            studio=self.studio,
            country=self.country,
            language=self.lang,
        )
        self.assertTrue(movie.slug)

    def test_review_bounds(self):
        user = User.objects.create_user(username="r1", password="Pass12345!")
        movie = Movie.objects.create(
            title="Film 2",
            synopsis="x",
            release_year=2025,
            duration_minutes=90,
            age_rating=self.age,
            studio=self.studio,
            country=self.country,
            language=self.lang,
        )
        review = Review(user=user, movie=movie, title="ok", body="good", rating=5)
        review.full_clean()


class WebPermissionsTests(TestCase):
    def setUp(self):
        self.country = Country.objects.create(name="PermCountry", code="PC")
        self.lang = Language.objects.create(name="PermLang", code="pl")
        self.age = AgeRating.objects.create(code="15+", description="perm")
        self.studio = Studio.objects.create(name="PermStudio", country=self.country)
        self.movie = Movie.objects.create(
            title="Perm Movie",
            synopsis="perm",
            release_year=2024,
            duration_minutes=95,
            age_rating=self.age,
            studio=self.studio,
            country=self.country,
            language=self.lang,
        )
        self.user = User.objects.create_user(username="regular", password="Pass12345!")
        self.staff = User.objects.create_user(
            username="staff_web", password="Pass12345!", is_staff=True
        )

    def test_anonymous_restricted_pages_redirect(self):
        response = self.client.get(reverse("movies:create"))
        self.assertEqual(response.status_code, 302)

        response = self.client.get(reverse("favorites:list"))
        self.assertEqual(response.status_code, 302)

        response = self.client.get(reverse("dashboard:panel"))
        self.assertEqual(response.status_code, 302)

    def test_regular_user_forbidden_on_staff_pages(self):
        self.client.login(username="regular", password="Pass12345!")
        response = self.client.get(reverse("movies:create"))
        self.assertEqual(response.status_code, 403)

        response = self.client.get(reverse("dashboard:panel"))
        self.assertEqual(response.status_code, 302)

    def test_staff_can_access_staff_pages(self):
        self.client.login(username="staff_web", password="Pass12345!")
        response = self.client.get(reverse("movies:create"))
        self.assertEqual(response.status_code, 200)

        response = self.client.get(reverse("dashboard:panel"))
        self.assertEqual(response.status_code, 200)
