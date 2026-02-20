from django import forms

from .models import Movie


class MovieForm(forms.ModelForm):
    class Meta:
        model = Movie
        fields = [
            "title",
            "synopsis",
            "release_year",
            "duration_minutes",
            "age_rating",
            "studio",
            "country",
            "language",
            "genres",
            "is_featured",
        ]
        widgets = {
            "genres": forms.CheckboxSelectMultiple(),
        }
