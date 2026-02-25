from django.urls import path

from .views import vote_toggle

urlpatterns = [
    path("toggle/", vote_toggle, name="toggle"),
]
