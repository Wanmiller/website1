from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.urls import include, path

from accounts.views import profile

urlpatterns = [
    path("admin/", admin.site.urls),
    path("i18n/", include("django.conf.urls.i18n")),
    path("", include(("core.urls", "core"), namespace="core")),
    path("auth/", include(("accounts.urls", "accounts"), namespace="accounts")),
    path("profile/", login_required(profile), name="profile"),
    path("people/", include(("people.urls", "people"), namespace="people")),
    path("search/", include(("search.urls", "search"), namespace="search")),
    path("threads/", include(("threads.urls", "threads"), namespace="threads")),
    path("bookmarks/", include(("engagement.urls", "engagement"), namespace="engagement")),
    path("comments/", include(("comments.urls", "comments"), namespace="comments")),
    path("votes/", include(("votes.urls", "votes"), namespace="votes")),
    path("moderation/", include(("moderation.urls", "moderation"), namespace="moderation")),
    path("dashboard/", include(("dashboard.urls", "dashboard"), namespace="dashboard")),
    path("api/v1/", include(("api.urls", "api"), namespace="api")),
]

handler404 = "core.views.handler404"
handler500 = "core.views.handler500"

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
