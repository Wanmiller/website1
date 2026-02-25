from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from people.models import Person
from threads.models import Thread


class SearchTests(TestCase):
    def setUp(self):
        user = User.objects.create_user(username="search_user", password="Pass12345!")
        person = Person.objects.create(full_name="Search Person")
        Thread.objects.create(author=user, person=person, title="Search Thread", body="Body")

    def test_search_page(self):
        response = self.client.get(reverse("search:page"), {"q": "Search"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Search")

    def test_live_search(self):
        response = self.client.get(reverse("search:live"), {"q": "Search"})
        self.assertEqual(response.status_code, 200)
        self.assertIn("results", response.json())
