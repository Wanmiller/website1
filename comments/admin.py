from django.contrib import admin

from .models import Comment


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("id", "thread", "author", "parent", "status", "created_at")
    list_filter = ("status", "created_at")
    search_fields = ("body", "author__username", "thread__title")
