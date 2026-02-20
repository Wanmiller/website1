from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from favorites.models import Favorite
from movies.models import AgeRating, Country, Language, Movie, Studio


class FavoritesFlowTests(TestCase):
    def setUp(self):
        country = Country.objects.create(name="BB", code="BB")
        lang = Language.objects.create(name="EN", code="en")
        age = AgeRating.objects.create(code="18+", description="desc")
        studio = Studio.objects.create(name="Studio3", country=country)
        self.movie = Movie.objects.create(
            title="Fav Film",
            synopsis="x",
            release_year=2022,
            duration_minutes=110,
            age_rating=age,
            studio=studio,
            country=country,
            language=lang,
        )
        self.user = User.objects.create_user(username="favuser", password="Pass12345!")

    def test_toggle_favorite(self):
        self.client.login(username="favuser", password="Pass12345!")
        self.client.get(reverse("favorites:toggle", kwargs={"slug": self.movie.slug}))
        self.assertTrue(Favorite.objects.filter(user=self.user, movie=self.movie).exists())
