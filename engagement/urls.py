from django.urls import path

from .views import bookmark_list, bookmark_toggle, rating_set

app_name = "engagement"

urlpatterns = [
    path("", bookmark_list, name="list"),
    path("toggle/<slug:slug>/", bookmark_toggle, name="toggle"),
    path("rate/<slug:slug>/", rating_set, name="rate"),
]
