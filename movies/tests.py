from django.contrib.auth.models import User
from django.test import TestCase

from comments.models import Comment
from people.models import Person
from threads.models import Thread
from votes.models import Vote


class PersonaModelsTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="model_user", password="Pass12345!")
        self.person = Person.objects.create(full_name="Model Person", bio="bio")

    def test_person_slug_generated(self):
        self.assertTrue(self.person.slug)

    def test_thread_slug_generated(self):
        thread = Thread.objects.create(
            author=self.user,
            person=self.person,
            title="My first persona thread",
            body="content",
        )
        self.assertTrue(thread.slug)

    def test_vote_unique_per_user_target(self):
        thread = Thread.objects.create(author=self.user, person=self.person, title="t", body="b")
        Vote.objects.create(user=self.user, thread=thread, value=1)
        vote = Vote.objects.get(user=self.user, thread=thread)
        vote.value = -1
        vote.save()
        self.assertEqual(Vote.objects.filter(user=self.user, thread=thread).count(), 1)

    def test_comment_reply(self):
        thread = Thread.objects.create(author=self.user, person=self.person, title="t2", body="b2")
        parent = Comment.objects.create(thread=thread, author=self.user, body="parent")
        reply = Comment.objects.create(thread=thread, author=self.user, parent=parent, body="child")
        self.assertEqual(reply.parent, parent)
