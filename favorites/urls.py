from django.urls import path

from .views import favorites_list, toggle_favorite, toggle_favorite_ajax

urlpatterns = [
    path("", favorites_list, name="list"),
    path("toggle/<slug:slug>/", toggle_favorite, name="toggle"),
    path("toggle-ajax/<slug:slug>/", toggle_favorite_ajax, name="toggle_ajax"),
]
