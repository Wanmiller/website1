from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from people.models import Person

from .models import Thread


class ThreadCrudPermissionTests(TestCase):
    def setUp(self):
        self.author = User.objects.create_user(username="author", password="Pass12345!")
        self.other = User.objects.create_user(username="other", password="Pass12345!")
        self.staff = User.objects.create_user(
            username="staff_user",
            password="Pass12345!",
            is_staff=True,
        )
        self.person = Person.objects.create(full_name="Test Person")
        self.thread = Thread.objects.create(
            author=self.author,
            person=self.person,
            title="Original title",
            body="Original body",
        )

    def test_author_can_edit_thread(self):
        self.client.login(username="author", password="Pass12345!")
        response = self.client.post(
            reverse("threads:edit", kwargs={"slug": self.thread.slug}),
            {"person": self.person.id, "title": "Updated title", "body": "Updated body"},
        )
        self.assertEqual(response.status_code, 302)
        self.thread.refresh_from_db()
        self.assertEqual(self.thread.title, "Updated title")

    def test_non_author_cannot_edit_thread(self):
        self.client.login(username="other", password="Pass12345!")
        response = self.client.post(
            reverse("threads:edit", kwargs={"slug": self.thread.slug}),
            {"person": self.person.id, "title": "Hacked title", "body": "x"},
        )
        self.assertEqual(response.status_code, 302)
        self.thread.refresh_from_db()
        self.assertEqual(self.thread.title, "Original title")

    def test_staff_can_edit_thread(self):
        self.client.login(username="staff_user", password="Pass12345!")
        response = self.client.post(
            reverse("threads:edit", kwargs={"slug": self.thread.slug}),
            {"person": self.person.id, "title": "Staff edit", "body": "Body"},
        )
        self.assertEqual(response.status_code, 302)
        self.thread.refresh_from_db()
        self.assertEqual(self.thread.title, "Staff edit")

    def test_author_can_delete_thread(self):
        self.client.login(username="author", password="Pass12345!")
        response = self.client.post(reverse("threads:delete", kwargs={"slug": self.thread.slug}))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Thread.objects.filter(pk=self.thread.pk).exists())

    def test_non_author_cannot_delete_thread(self):
        self.client.login(username="other", password="Pass12345!")
        response = self.client.post(reverse("threads:delete", kwargs={"slug": self.thread.slug}))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Thread.objects.filter(pk=self.thread.pk).exists())

    def test_detail_shows_manage_actions_for_author(self):
        self.client.login(username="author", password="Pass12345!")
        response = self.client.get(reverse("threads:detail", kwargs={"slug": self.thread.slug}))
        self.assertContains(response, reverse("threads:edit", kwargs={"slug": self.thread.slug}))
        self.assertContains(response, reverse("threads:delete", kwargs={"slug": self.thread.slug}))

    def test_detail_hides_manage_actions_for_other_user(self):
        self.client.login(username="other", password="Pass12345!")
        response = self.client.get(reverse("threads:detail", kwargs={"slug": self.thread.slug}))
        self.assertNotContains(response, reverse("threads:edit", kwargs={"slug": self.thread.slug}))
        self.assertNotContains(response, reverse("threads:delete", kwargs={"slug": self.thread.slug}))

    def test_anonymous_user_redirected_from_edit_and_delete(self):
        edit_response = self.client.get(reverse("threads:edit", kwargs={"slug": self.thread.slug}))
        delete_response = self.client.get(reverse("threads:delete", kwargs={"slug": self.thread.slug}))
        self.assertEqual(edit_response.status_code, 302)
        self.assertEqual(delete_response.status_code, 302)
