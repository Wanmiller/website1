from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse


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

    def test_logout_get_works(self):
        user = User.objects.create_user(username="logout_user", password="Pass12345!")
        self.client.login(username="logout_user", password="Pass12345!")
        response = self.client.get(reverse("accounts:logout"))
        self.assertEqual(response.status_code, 302)
