from django.contrib import admin

from .models import (
    Attachment,
    Bookmark,
    Follow,
    Notification,
    Rating,
    Tag,
    ThreadTag,
    ViewEvent,
)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "created_at")
    search_fields = ("name",)
    prepopulated_fields = {"slug": ("name",)}


@admin.register(ThreadTag)
class ThreadTagAdmin(admin.ModelAdmin):
    list_display = ("thread", "tag", "created_at")
    list_filter = ("created_at",)
    search_fields = ("thread__title", "tag__name")


@admin.register(Bookmark)
class BookmarkAdmin(admin.ModelAdmin):
    list_display = ("user", "thread", "created_at")
    list_filter = ("created_at",)
    search_fields = ("user__username", "thread__title")


@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ("user", "thread", "value", "updated_at")
    list_filter = ("value", "updated_at")
    search_fields = ("user__username", "thread__title")


@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    list_display = ("follower", "person", "created_at")
    list_filter = ("created_at",)
    search_fields = ("follower__username", "person__full_name")


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ("user", "kind", "is_read", "created_at")
    list_filter = ("kind", "is_read", "created_at")
    search_fields = ("user__username", "title")
    actions = ("mark_read",)

    @admin.action(description="Mark selected notifications as read")
    def mark_read(self, request, queryset):
        queryset.update(is_read=True)


@admin.register(Attachment)
class AttachmentAdmin(admin.ModelAdmin):
    list_display = ("id", "thread", "uploaded_by", "created_at")
    list_filter = ("created_at",)
    search_fields = ("thread__title", "uploaded_by__username", "alt_text")


@admin.register(ViewEvent)
class ViewEventAdmin(admin.ModelAdmin):
    list_display = ("thread", "user", "ip_address", "created_at")
    list_filter = ("created_at",)
    search_fields = ("thread__title", "user__username", "ip_address")
