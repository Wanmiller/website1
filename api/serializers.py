from rest_framework import serializers

from favorites.models import Favorite
from movies.models import Movie
from reviews.models import Review


class MovieSerializer(serializers.ModelSerializer):
    genres = serializers.StringRelatedField(many=True)
    average_rating = serializers.SerializerMethodField()

    class Meta:
        model = Movie
        fields = (
            "id",
            "title",
            "slug",
            "release_year",
            "duration_minutes",
            "genres",
            "average_rating",
        )

    def get_average_rating(self, obj):
        value = getattr(obj, "avg_rating", None)
        if value is None:
            return obj.average_rating
        return round(value or 0, 2)


class MovieDetailSerializer(serializers.ModelSerializer):
    genres = serializers.StringRelatedField(many=True)
    trailers = serializers.StringRelatedField(many=True)

    class Meta:
        model = Movie
        fields = (
            "id",
            "title",
            "slug",
            "synopsis",
            "release_year",
            "duration_minutes",
            "genres",
            "trailers",
        )


class MovieWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = (
            "title",
            "synopsis",
            "release_year",
            "duration_minutes",
            "age_rating",
            "studio",
            "country",
            "language",
            "genres",
            "is_featured",
        )


class ReviewSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Review
        fields = ("id", "movie", "user", "title", "body", "rating", "created_at")
        read_only_fields = ("user",)


class FavoriteSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    movie_title = serializers.CharField(source="movie.title", read_only=True)

    class Meta:
        model = Favorite
        fields = ("id", "user", "movie", "movie_title", "created_at")
        read_only_fields = ("user",)
