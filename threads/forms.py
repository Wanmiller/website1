from django import forms
from django.utils.translation import gettext_lazy as _

from .models import Thread


class ThreadForm(forms.ModelForm):
    class Meta:
        model = Thread
        fields = ["person", "title", "body"]
        labels = {
            "person": _("Person"),
            "title": _("Title"),
            "body": _("Body"),
        }
        widgets = {
            "body": forms.Textarea(attrs={"rows": 6}),
        }
