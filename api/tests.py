import json

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from movies.models import AgeRating, Country, Language, Movie, Studio


class APITests(TestCase):
    def setUp(self):
        self.country = Country.objects.create(name="AA", code="AA")
        self.lang = Language.objects.create(name="LL", code="ll")
        self.age = AgeRating.objects.create(code="16+", description="desc")
        self.studio = Studio.objects.create(name="Studio2", country=self.country)
        self.movie = Movie.objects.create(
            title="API Film",
            synopsis="desc",
            release_year=2023,
            duration_minutes=102,
            age_rating=self.age,
            studio=self.studio,
            country=self.country,
            language=self.lang,
        )
        self.user = User.objects.create_user(username="u2", password="Pass12345!")
        self.staff = User.objects.create_user(
            username="staff_api", password="Pass12345!", is_staff=True
        )

    def test_movie_list(self):
        response = self.client.get(reverse("api:movies"))
        self.assertEqual(response.status_code, 200)

    def test_protected_favorites(self):
        response = self.client.get(reverse("api:favorites"))
        self.assertEqual(response.status_code, 403)

    def test_create_review_auth(self):
        self.client.login(username="u2", password="Pass12345!")
        response = self.client.post(
            reverse("api:reviews"),
            {"movie": self.movie.id, "title": "T", "body": "B", "rating": 4},
        )
        self.assertEqual(response.status_code, 201)

    def test_movies_post_forbidden_for_anonymous(self):
        payload = {
            "title": "Anon Create",
            "synopsis": "Denied",
            "release_year": 2024,
            "duration_minutes": 100,
            "age_rating": self.age.id,
            "studio": self.studio.id,
            "country": self.country.id,
            "language": self.lang.id,
            "genres": [],
            "is_featured": False,
        }
        response = self.client.post(
            reverse("api:movies"), data=json.dumps(payload), content_type="application/json"
        )
        self.assertEqual(response.status_code, 403)

    def test_movies_post_forbidden_for_non_staff(self):
        self.client.login(username="u2", password="Pass12345!")
        payload = {
            "title": "User Create",
            "synopsis": "Denied",
            "release_year": 2024,
            "duration_minutes": 100,
            "age_rating": self.age.id,
            "studio": self.studio.id,
            "country": self.country.id,
            "language": self.lang.id,
            "genres": [],
            "is_featured": False,
        }
        response = self.client.post(
            reverse("api:movies"), data=json.dumps(payload), content_type="application/json"
        )
        self.assertEqual(response.status_code, 403)

    def test_movies_post_allowed_for_staff(self):
        self.client.login(username="staff_api", password="Pass12345!")
        payload = {
            "title": "Staff Create",
            "synopsis": "Allowed",
            "release_year": 2024,
            "duration_minutes": 100,
            "age_rating": self.age.id,
            "studio": self.studio.id,
            "country": self.country.id,
            "language": self.lang.id,
            "genres": [],
            "is_featured": True,
        }
        response = self.client.post(
            reverse("api:movies"), data=json.dumps(payload), content_type="application/json"
        )
        self.assertEqual(response.status_code, 201)
