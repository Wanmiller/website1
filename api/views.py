from django.db.models import Avg, Count, IntegerField, Q, Sum, Value
from django.db.models.functions import Coalesce
from django.utils.dateparse import parse_date, parse_datetime
from django.utils.timezone import is_naive, make_aware
from rest_framework import generics, permissions, status
from rest_framework.response import Response

from comments.models import Comment
from engagement.models import Bookmark, Rating
from moderation.models import Report
from people.models import Person
from threads.models import Thread
from votes.models import Vote

from .serializers import (
    BookmarkSerializer,
    CommentSerializer,
    PersonSerializer,
    RatingSerializer,
    ReportSerializer,
    ThreadSerializer,
    VoteSerializer,
)


def _annotated_threads_queryset():
    return Thread.objects.select_related("author", "person").annotate(
        vote_score=Coalesce(Sum("votes__value"), Value(0), output_field=IntegerField()),
        avg_rating=Coalesce(Avg("ratings__value"), Value(0.0)),
        comments_count=Count(
            "comments",
            filter=Q(comments__status=Comment.STATUS_PUBLISHED),
            distinct=True,
        ),
    )


class PersonListAPIView(generics.ListAPIView):
    serializer_class = PersonSerializer

    def get_queryset(self):
        q = self.request.GET.get("q", "").strip()
        qs = Person.objects.all()
        if q:
            qs = qs.filter(full_name__icontains=q)
        return qs


class ThreadListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = ThreadSerializer

    def get_permissions(self):
        if self.request.method == "POST":
            return [permissions.IsAuthenticated()]
        return [permissions.AllowAny()]

    def get_queryset(self):
        q = self.request.GET.get("q", "").strip()
        person_slug = self.request.GET.get("person", "").strip()
        ordering = self.request.GET.get("ordering", "hot").strip() or "hot"
        created_after = self.request.GET.get("created_after", "").strip()
        score_min = self.request.GET.get("score_min", "").strip()

        qs = _annotated_threads_queryset().filter(status=Thread.STATUS_PUBLISHED)
        if q:
            qs = qs.filter(Q(title__icontains=q) | Q(body__icontains=q))
        if person_slug:
            qs = qs.filter(person__slug=person_slug)

        if created_after:
            date_value = parse_date(created_after)
            if date_value is not None:
                qs = qs.filter(created_at__date__gte=date_value)
            else:
                dt_value = parse_datetime(created_after)
                if dt_value is not None:
                    if is_naive(dt_value):
                        dt_value = make_aware(dt_value)
                    qs = qs.filter(created_at__gte=dt_value)

        if score_min:
            try:
                qs = qs.filter(vote_score__gte=int(score_min))
            except ValueError:
                pass

        if ordering == "new":
            qs = qs.order_by("-created_at")
        elif ordering == "top":
            qs = qs.order_by("-vote_score", "-created_at")
        else:
            qs = qs.order_by("-vote_score", "-comments_count", "-created_at")
        return qs

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class ThreadDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ThreadSerializer
    lookup_field = "slug"

    def get_permissions(self):
        if self.request.method in permissions.SAFE_METHODS:
            return [permissions.AllowAny()]
        return [permissions.IsAdminUser()]

    def get_queryset(self):
        qs = _annotated_threads_queryset()
        if self.request.method in permissions.SAFE_METHODS and not self.request.user.is_staff:
            qs = qs.filter(status=Thread.STATUS_PUBLISHED)
        return qs


class CommentCreateAPIView(generics.CreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class VoteCreateAPIView(generics.CreateAPIView):
    serializer_class = VoteSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance, _ = Vote.objects.update_or_create(
            user=request.user,
            thread=serializer.validated_data.get("thread"),
            comment=serializer.validated_data.get("comment"),
            defaults={"value": serializer.validated_data["value"]},
        )
        output = self.get_serializer(instance)
        return Response(output.data, status=status.HTTP_200_OK)


class BookmarkCreateAPIView(generics.CreateAPIView):
    serializer_class = BookmarkSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance, _ = Bookmark.objects.get_or_create(
            user=request.user,
            thread=serializer.validated_data["thread"],
        )
        output = self.get_serializer(instance)
        return Response(output.data, status=status.HTTP_200_OK)


class RatingCreateAPIView(generics.CreateAPIView):
    serializer_class = RatingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance, _ = Rating.objects.update_or_create(
            user=request.user,
            thread=serializer.validated_data["thread"],
            defaults={"value": serializer.validated_data["value"]},
        )
        output = self.get_serializer(instance)
        return Response(output.data, status=status.HTTP_200_OK)


class ReportCreateAPIView(generics.CreateAPIView):
    serializer_class = ReportSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(reporter=self.request.user)
