import json
from datetime import timedelta

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from engagement.models import Bookmark, Rating
from people.models import Person
from threads.models import Thread


class APITests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="api_user", password="Pass12345!")
        self.staff = User.objects.create_user(
            username="api_staff", password="Pass12345!", is_staff=True
        )
        self.person = Person.objects.create(full_name="API Person", bio="bio")
        self.thread = Thread.objects.create(
            author=self.user,
            person=self.person,
            title="API Thread",
            body="desc",
        )

    def test_person_list(self):
        response = self.client.get(reverse("api:persons"))
        self.assertEqual(response.status_code, 200)

    def test_thread_list(self):
        response = self.client.get(reverse("api:threads"))
        self.assertEqual(response.status_code, 200)

    def test_thread_filters(self):
        response = self.client.get(
            reverse("api:threads"),
            {
                "q": "API",
                "person": self.person.slug,
                "ordering": "hot",
                "created_after": (timezone.now() - timedelta(days=1)).date().isoformat(),
                "score_min": 0,
            },
        )
        self.assertEqual(response.status_code, 200)

    def test_thread_create_requires_auth(self):
        payload = {"title": "No auth", "body": "x", "person_id": self.person.id}
        response = self.client.post(
            reverse("api:threads"), data=json.dumps(payload), content_type="application/json"
        )
        self.assertEqual(response.status_code, 403)

    def test_thread_create_for_authenticated_user(self):
        self.client.login(username="api_user", password="Pass12345!")
        payload = {"title": "Auth thread", "body": "x", "person_id": self.person.id}
        response = self.client.post(
            reverse("api:threads"), data=json.dumps(payload), content_type="application/json"
        )
        self.assertEqual(response.status_code, 201)

    def test_thread_update_requires_staff(self):
        self.client.login(username="api_user", password="Pass12345!")
        response = self.client.patch(
            reverse("api:thread_detail", kwargs={"slug": self.thread.slug}),
            data=json.dumps({"title": "new"}),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 403)

    def test_thread_update_for_staff(self):
        self.client.login(username="api_staff", password="Pass12345!")
        response = self.client.patch(
            reverse("api:thread_detail", kwargs={"slug": self.thread.slug}),
            data=json.dumps({"title": "Updated by staff"}),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)

    def test_comment_create_auth(self):
        self.client.login(username="api_user", password="Pass12345!")
        payload = {"thread": self.thread.id, "body": "comment"}
        response = self.client.post(
            reverse("api:comments"), data=json.dumps(payload), content_type="application/json"
        )
        self.assertEqual(response.status_code, 201)

    def test_vote_create_auth(self):
        self.client.login(username="api_user", password="Pass12345!")
        payload = {"thread": self.thread.id, "value": 1}
        response = self.client.post(
            reverse("api:votes"), data=json.dumps(payload), content_type="application/json"
        )
        self.assertEqual(response.status_code, 200)

    def test_bookmark_create_auth(self):
        self.client.login(username="api_user", password="Pass12345!")
        payload = {"thread": self.thread.id}
        response = self.client.post(
            reverse("api:bookmarks"), data=json.dumps(payload), content_type="application/json"
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Bookmark.objects.filter(user=self.user, thread=self.thread).exists())

    def test_rating_create_auth(self):
        self.client.login(username="api_user", password="Pass12345!")
        payload = {"thread": self.thread.id, "value": 4}
        response = self.client.post(
            reverse("api:ratings"), data=json.dumps(payload), content_type="application/json"
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Rating.objects.get(user=self.user, thread=self.thread).value, 4)

    def test_unified_error_format(self):
        response = self.client.get(reverse("api:thread_detail", kwargs={"slug": "missing-slug"}))
        self.assertEqual(response.status_code, 404)
        self.assertIn("error", response.json())
