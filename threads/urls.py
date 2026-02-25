from django.urls import path

from .views import (
    thread_comment_create,
    thread_create,
    thread_delete,
    thread_detail,
    thread_list,
    thread_update,
)

urlpatterns = [
    path("", thread_list, name="list"),
    path("create/", thread_create, name="create"),
    path("<slug:slug>/edit/", thread_update, name="edit"),
    path("<slug:slug>/delete/", thread_delete, name="delete"),
    path("<slug:slug>/", thread_detail, name="detail"),
    path("<slug:slug>/comment/", thread_comment_create, name="comment_create"),
]
