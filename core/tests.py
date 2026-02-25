from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from people.models import Person
from threads.models import Thread


class CoreViewsTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="core_user", password="Pass12345!")
        self.person = Person.objects.create(full_name="Core Person", bio="Bio", is_verified=True)
        self.thread = Thread.objects.create(
            author=self.user,
            person=self.person,
            title="Core thread",
            body="Thread body",
        )
        self.client.cookies["django_language"] = "en"

    def test_home_page(self):
        response = self.client.get(reverse("core:home"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Community Feed")

    def test_thread_list_page(self):
        response = self.client.get(reverse("threads:list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Threads")

    def test_thread_detail_page(self):
        response = self.client.get(reverse("threads:detail", kwargs={"slug": self.thread.slug}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.thread.title)
