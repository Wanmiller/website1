from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.urls import include, path

from accounts.views import profile

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include(("core.urls", "core"), namespace="core")),
    path("auth/", include(("accounts.urls", "accounts"), namespace="accounts")),
    path("profile/", login_required(profile), name="profile"),
    path("movies/", include(("movies.urls", "movies"), namespace="movies")),
    path("genres/", include(("genres.urls", "genres"), namespace="genres")),
    path("people/", include(("people.urls", "people"), namespace="people")),
    path("reviews/", include(("reviews.urls", "reviews"), namespace="reviews")),
    path("favorites/", include(("favorites.urls", "favorites"), namespace="favorites")),
    path("search/", include(("search.urls", "search"), namespace="search")),
    path("dashboard/", include(("dashboard.urls", "dashboard"), namespace="dashboard")),
    path("api/v1/", include(("api.urls", "api"), namespace="api")),
]

handler404 = "core.views.handler404"
handler500 = "core.views.handler500"

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
