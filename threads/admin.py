from django.contrib import admin

from engagement.models import ThreadTag

from .models import Thread


class ThreadTagInline(admin.TabularInline):
    model = ThreadTag
    extra = 1
    autocomplete_fields = ("tag",)


@admin.register(Thread)
class ThreadAdmin(admin.ModelAdmin):
    list_display = ("title", "person", "author", "status", "created_at")
    list_filter = ("status", "created_at")
    search_fields = ("title", "body", "person__full_name", "author__username")
    readonly_fields = ("created_at", "updated_at", "slug")
    fieldsets = (
        ("Main", {"fields": ("title", "person", "author", "body", "status")}),
        ("Meta", {"fields": ("slug", "created_at", "updated_at"), "classes": ("collapse",)}),
    )
    inlines = (ThreadTagInline,)
    actions = ("mark_published", "mark_hidden")

    @admin.action(description="Mark selected threads as published")
    def mark_published(self, request, queryset):
        queryset.update(status=Thread.STATUS_PUBLISHED)

    @admin.action(description="Mark selected threads as hidden")
    def mark_hidden(self, request, queryset):
        queryset.update(status=Thread.STATUS_HIDDEN)
