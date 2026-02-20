from django.contrib import admin

from .models import (
    AgeRating,
    Country,
    Language,
    Movie,
    MovieImage,
    MovieTag,
    Studio,
    Tag,
    Trailer,
    WatchlistEvent,
)


class TrailerInline(admin.TabularInline):
    model = Trailer
    extra = 1


class MovieImageInline(admin.TabularInline):
    model = MovieImage
    extra = 1


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ("title", "release_year", "studio", "age_rating", "is_featured", "created_at")
    list_filter = ("release_year", "is_featured", "age_rating", "genres")
    search_fields = ("title", "synopsis")
    prepopulated_fields = {"slug": ("title",)}
    readonly_fields = ("created_at", "updated_at")
    fieldsets = (
        ("Main", {"fields": ("title", "slug", "synopsis", "release_year", "duration_minutes")}),
        ("Relations", {"fields": ("age_rating", "studio", "country", "language", "genres")}),
        ("Flags", {"fields": ("is_featured",)}),
        ("Timestamps", {"fields": ("created_at", "updated_at")}),
    )
    inlines = [TrailerInline, MovieImageInline]
    actions = ["mark_featured", "unmark_featured"]

    @admin.action(description="Mark selected movies as featured")
    def mark_featured(self, request, queryset):
        queryset.update(is_featured=True)

    @admin.action(description="Mark selected movies as not featured")
    def unmark_featured(self, request, queryset):
        queryset.update(is_featured=False)


@admin.register(Studio)
class StudioAdmin(admin.ModelAdmin):
    list_display = ("name", "country")
    search_fields = ("name",)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")
    search_fields = ("name",)
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = ("name", "code")
    search_fields = ("name", "code")


@admin.register(Language)
class LanguageAdmin(admin.ModelAdmin):
    list_display = ("name", "code")
    search_fields = ("name", "code")


@admin.register(AgeRating)
class AgeRatingAdmin(admin.ModelAdmin):
    list_display = ("code", "description")
    search_fields = ("code",)


admin.site.register(MovieImage)
admin.site.register(Trailer)
admin.site.register(MovieTag)
admin.site.register(WatchlistEvent)
