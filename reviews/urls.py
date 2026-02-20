from django.urls import path

from .views import my_reviews, review_ajax_rate, review_create, review_list

urlpatterns = [
    path("", review_list, name="list"),
    path("mine/", my_reviews, name="my_reviews"),
    path("create/", review_create, name="create"),
    path("ajax/rate/<int:movie_id>/", review_ajax_rate, name="ajax_rate"),
]
