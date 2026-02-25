from django.contrib.auth.models import User
from django.core.cache import cache
from django.test import TestCase, override_settings
from django.urls import reverse

from comments.models import Comment
from engagement.models import Bookmark, Rating
from people.models import Person
from threads.models import Thread


class AccountsTests(TestCase):
    def test_register(self):
        response = self.client.post(
            reverse("accounts:register"),
            {
                "username": "u1",
                "email": "u1@example.com",
                "password1": "StrongPass123!",
                "password2": "StrongPass123!",
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(username="u1").exists())

    def test_logout_requires_post(self):
        user = User.objects.create_user(username="logout_user", password="Pass12345!")
        self.client.login(username="logout_user", password="Pass12345!")
        get_response = self.client.get(reverse("accounts:logout"))
        self.assertEqual(get_response.status_code, 405)
        post_response = self.client.post(reverse("accounts:logout"))
        self.assertEqual(post_response.status_code, 302)

    @override_settings(LOGIN_MAX_ATTEMPTS=2, LOGIN_LOCKOUT_SECONDS=120)
    def test_login_rate_limit_blocks_after_threshold(self):
        cache.clear()
        User.objects.create_user(username="limited_user", password="Pass12345!")
        login_url = reverse("accounts:login")

        self.client.post(login_url, {"username": "limited_user", "password": "wrong"})
        self.client.post(login_url, {"username": "limited_user", "password": "wrong"})
        response = self.client.post(
            login_url,
            {"username": "limited_user", "password": "Pass12345!"},
            follow=True,
        )

        self.assertFalse(response.wsgi_request.user.is_authenticated)
        self.assertContains(response, "Too many login attempts")

    @override_settings(LOGIN_MAX_ATTEMPTS=3, LOGIN_LOCKOUT_SECONDS=120)
    def test_successful_login_resets_rate_limit(self):
        cache.clear()
        User.objects.create_user(username="reset_user", password="Pass12345!")
        login_url = reverse("accounts:login")

        self.client.post(login_url, {"username": "reset_user", "password": "wrong"})
        success = self.client.post(
            login_url,
            {"username": "reset_user", "password": "Pass12345!"},
            follow=True,
        )
        self.assertTrue(success.wsgi_request.user.is_authenticated)

        self.client.post(reverse("accounts:logout"))
        second_success = self.client.post(
            login_url,
            {"username": "reset_user", "password": "Pass12345!"},
            follow=True,
        )
        self.assertTrue(second_success.wsgi_request.user.is_authenticated)

    def test_profile_contains_user_activity_sections(self):
        user = User.objects.create_user(username="profile_user", password="Pass12345!")
        person = Person.objects.create(full_name="Profile Person")
        thread = Thread.objects.create(
            author=user,
            person=person,
            title="Profile thread",
            body="Body",
        )
        Comment.objects.create(thread=thread, author=user, body="My comment")
        Bookmark.objects.create(user=user, thread=thread)
        Rating.objects.create(user=user, thread=thread, value=4)

        self.client.login(username="profile_user", password="Pass12345!")
        response = self.client.get(reverse("accounts:profile"))
        self.assertContains(response, "Profile thread")
        self.assertContains(response, "4/5")
