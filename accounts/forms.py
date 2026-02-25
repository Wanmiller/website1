from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

from .models import UserProfile


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True, label=_("Email"))

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("username", "email", "first_name", "last_name")
        labels = {
            "username": _("Username"),
            "email": _("Email"),
            "first_name": _("First name"),
            "last_name": _("Last name"),
        }


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ("display_name", "bio", "avatar")
        labels = {
            "display_name": _("Display name"),
            "bio": _("Bio"),
            "avatar": _("Avatar"),
        }
