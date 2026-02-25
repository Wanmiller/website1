from django.contrib import admin

from .models import Person


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    list_display = ("full_name", "slug", "is_verified", "birth_date")
    list_filter = ("is_verified",)
    search_fields = ("full_name", "bio")
    readonly_fields = ("slug",)
