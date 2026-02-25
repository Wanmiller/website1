from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from people.models import Person
from threads.models import Thread


class ThreadsFlowTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="flow_user", password="Pass12345!")
        self.person = Person.objects.create(full_name="Flow Person", bio="bio")
        self.thread = Thread.objects.create(
            author=self.user,
            person=self.person,
            title="Flow thread",
            body="flow body",
        )

    def test_thread_create_requires_login(self):
        response = self.client.get(reverse("threads:create"))
        self.assertEqual(response.status_code, 302)

    def test_reply_requires_login(self):
        from comments.models import Comment

        comment = Comment.objects.create(thread=self.thread, author=self.user, body="x")
        response = self.client.get(reverse("comments:reply", kwargs={"pk": comment.pk}))
        self.assertEqual(response.status_code, 302)
