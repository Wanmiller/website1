from django.db.models import Avg, Q
from rest_framework import filters, generics, permissions

from favorites.models import Favorite
from movies.models import Movie
from reviews.models import Review

from .serializers import (
    FavoriteSerializer,
    MovieDetailSerializer,
    MovieSerializer,
    MovieWriteSerializer,
    ReviewSerializer,
)


class IsStaffOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user and request.user.is_staff


class MovieListCreateAPIView(generics.ListCreateAPIView):
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ["title", "release_year"]

    def get_serializer_class(self):
        if self.request.method == "POST":
            return MovieWriteSerializer
        return MovieSerializer

    def get_permissions(self):
        if self.request.method == "POST":
            return [IsStaffOrReadOnly()]
        return [permissions.AllowAny()]

    def get_queryset(self):
        qs = (
            Movie.objects.prefetch_related("genres")
            .annotate(avg_rating=Avg("reviews__rating"))
            .all()
        )
        q = self.request.GET.get("q")
        genre = self.request.GET.get("genre")
        year = self.request.GET.get("year")
        rating_min = self.request.GET.get("rating_min")

        if q:
            qs = qs.filter(Q(title__icontains=q) | Q(synopsis__icontains=q))
        if genre:
            qs = qs.filter(genres__slug=genre)
        if year:
            qs = qs.filter(release_year=year)
        if rating_min:
            qs = qs.filter(reviews__rating__gte=rating_min)

        return qs.distinct()


class MovieDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Movie.objects.prefetch_related("genres", "trailers")
    lookup_field = "slug"

    def get_serializer_class(self):
        if self.request.method in permissions.SAFE_METHODS:
            return MovieDetailSerializer
        return MovieWriteSerializer

    def get_permissions(self):
        if self.request.method in permissions.SAFE_METHODS:
            return [permissions.AllowAny()]
        return [IsStaffOrReadOnly()]


class ReviewListCreateAPIView(generics.ListCreateAPIView):
    queryset = Review.objects.select_related("movie", "user")
    serializer_class = ReviewSerializer

    def get_permissions(self):
        if self.request.method == "POST":
            return [permissions.IsAuthenticated()]
        return [permissions.AllowAny()]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class FavoriteListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = FavoriteSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Favorite.objects.filter(user=self.request.user).select_related("movie")

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class SearchAPIView(generics.ListAPIView):
    serializer_class = MovieSerializer

    def get_queryset(self):
        q = self.request.GET.get("q", "")
        return Movie.objects.filter(title__icontains=q).prefetch_related("genres")[:20]
