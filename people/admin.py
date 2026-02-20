from django.contrib import admin

from .models import Person, RoleCredit


class RoleCreditInline(admin.TabularInline):
    model = RoleCredit
    extra = 1


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    list_display = ("full_name", "birth_date")
    search_fields = ("full_name",)
    inlines = [RoleCreditInline]


@admin.register(RoleCredit)
class RoleCreditAdmin(admin.ModelAdmin):
    list_display = ("movie", "person", "role")
    list_filter = ("role",)
    search_fields = ("movie__title", "person__full_name")
