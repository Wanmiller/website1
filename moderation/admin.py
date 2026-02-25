from django.contrib import admin

from .models import Report


@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ("target_type", "target_id", "reporter", "status", "created_at")
    list_filter = ("target_type", "status", "created_at")
    search_fields = ("reason", "reporter__username")
