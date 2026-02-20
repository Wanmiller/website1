from django.urls import path

from .views import genre_detail, genre_list

urlpatterns = [
    path("", genre_list, name="list"),
    path("<slug:slug>/", genre_detail, name="detail"),
]
