from django.urls import path

from .views import live_search, search_page

urlpatterns = [
    path("", search_page, name="page"),
    path("live/", live_search, name="live"),
]
