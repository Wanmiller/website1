from django.urls import path

from .views import (
    BookmarkCreateAPIView,
    CommentCreateAPIView,
    PersonListAPIView,
    RatingCreateAPIView,
    ReportCreateAPIView,
    ThreadDetailAPIView,
    ThreadListCreateAPIView,
    VoteCreateAPIView,
)

urlpatterns = [
    path("persons/", PersonListAPIView.as_view(), name="persons"),
    path("threads/", ThreadListCreateAPIView.as_view(), name="threads"),
    path("threads/<slug:slug>/", ThreadDetailAPIView.as_view(), name="thread_detail"),
    path("comments/", CommentCreateAPIView.as_view(), name="comments"),
    path("votes/", VoteCreateAPIView.as_view(), name="votes"),
    path("bookmarks/", BookmarkCreateAPIView.as_view(), name="bookmarks"),
    path("ratings/", RatingCreateAPIView.as_view(), name="ratings"),
    path("reports/", ReportCreateAPIView.as_view(), name="reports"),
]
