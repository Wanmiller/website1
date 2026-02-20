from django.urls import path

from .views import (
    FavoriteListCreateAPIView,
    MovieDetailAPIView,
    MovieListCreateAPIView,
    ReviewListCreateAPIView,
    SearchAPIView,
)

urlpatterns = [
    path("movies/", MovieListCreateAPIView.as_view(), name="movies"),
    path("movies/<slug:slug>/", MovieDetailAPIView.as_view(), name="movie_detail"),
    path("reviews/", ReviewListCreateAPIView.as_view(), name="reviews"),
    path("favorites/", FavoriteListCreateAPIView.as_view(), name="favorites"),
    path("search/", SearchAPIView.as_view(), name="search"),
]
