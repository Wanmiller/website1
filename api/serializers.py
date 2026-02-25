from rest_framework import serializers
from django.utils.translation import gettext_lazy as _

from comments.models import Comment
from engagement.models import Bookmark, Rating
from moderation.models import Report
from people.models import Person
from threads.models import Thread
from votes.models import Vote


class PersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = ("id", "full_name", "slug", "bio", "is_verified")


class ThreadSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)
    person = PersonSerializer(read_only=True)
    person_id = serializers.PrimaryKeyRelatedField(
        source="person", queryset=Person.objects.all(), write_only=True
    )
    score = serializers.SerializerMethodField()
    average_rating = serializers.SerializerMethodField()

    class Meta:
        model = Thread
        fields = (
            "id",
            "title",
            "slug",
            "body",
            "author",
            "person",
            "person_id",
            "status",
            "created_at",
            "updated_at",
            "score",
            "average_rating",
        )
        read_only_fields = (
            "author",
            "status",
            "slug",
            "created_at",
            "updated_at",
            "score",
            "average_rating",
        )

    def get_score(self, obj):
        value = getattr(obj, "vote_score", None)
        if value is None:
            return obj.score
        return int(value or 0)

    def get_average_rating(self, obj):
        value = getattr(obj, "avg_rating", None)
        if value is None:
            return float(obj.average_rating or 0)
        return float(value or 0)


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Comment
        fields = (
            "id",
            "thread",
            "author",
            "parent",
            "body",
            "status",
            "created_at",
            "updated_at",
        )
        read_only_fields = ("author", "status", "created_at", "updated_at")


class VoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vote
        fields = ("id", "thread", "comment", "value", "created_at", "updated_at")
        read_only_fields = ("created_at", "updated_at")

    def validate(self, attrs):
        thread = attrs.get("thread")
        comment = attrs.get("comment")
        if bool(thread) == bool(comment):
            raise serializers.ValidationError(_("Provide exactly one target: thread or comment."))
        if attrs.get("value") not in (-1, 1):
            raise serializers.ValidationError(_("Value must be -1 or 1."))
        return attrs


class ReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Report
        fields = ("id", "target_type", "target_id", "reason", "status", "created_at")
        read_only_fields = ("status", "created_at")


class BookmarkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bookmark
        fields = ("id", "thread", "created_at")
        read_only_fields = ("created_at",)


class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = ("id", "thread", "value", "created_at", "updated_at")
        read_only_fields = ("created_at", "updated_at")
