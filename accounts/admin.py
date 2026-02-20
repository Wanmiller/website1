from django.contrib import admin

from .models import LoginAudit, UserProfile


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "display_name")
    search_fields = ("user__username", "display_name")


@admin.register(LoginAudit)
class LoginAuditAdmin(admin.ModelAdmin):
    list_display = ("user", "created_at", "ip_address")
    list_filter = ("created_at",)
    search_fields = ("user__username", "ip_address")
