from django.urls import path

from .views import (
    MovieCreateView,
    MovieDeleteView,
    MovieUpdateView,
    movie_detail,
    movie_list,
    movie_stats,
)

urlpatterns = [
    path("", movie_list, name="list"),
    path("stats/", movie_stats, name="stats"),
    path("create/", MovieCreateView.as_view(), name="create"),
    path("<slug:slug>/", movie_detail, name="detail"),
    path("<slug:slug>/edit/", MovieUpdateView.as_view(), name="edit"),
    path("<slug:slug>/delete/", MovieDeleteView.as_view(), name="delete"),
]
