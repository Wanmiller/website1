from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from engagement.models import Bookmark, Rating
from people.models import Person
from threads.models import Thread


class EngagementViewsTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="eng_user", password="Pass12345!")
        person = Person.objects.create(full_name="Eng Person")
        self.thread = Thread.objects.create(
            author=self.user,
            person=person,
            title="Eng Thread",
            body="text",
        )

    def test_bookmark_toggle_requires_login(self):
        response = self.client.post(reverse("engagement:toggle", kwargs={"slug": self.thread.slug}))
        self.assertEqual(response.status_code, 302)

    def test_bookmark_toggle(self):
        self.client.login(username="eng_user", password="Pass12345!")
        url = reverse("engagement:toggle", kwargs={"slug": self.thread.slug})
        response = self.client.post(url)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Bookmark.objects.filter(user=self.user, thread=self.thread).exists())

    def test_rating_set(self):
        self.client.login(username="eng_user", password="Pass12345!")
        url = reverse("engagement:rate", kwargs={"slug": self.thread.slug})
        response = self.client.post(url, {"rating": 5})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Rating.objects.get(user=self.user, thread=self.thread).value, 5)
