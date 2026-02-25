from django.contrib.auth.decorators import login_required
from django.db.models import Avg
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.utils.translation import gettext as _
from django.views.decorators.http import require_POST

from core.templatetags.core_extras import rating_badge
from threads.models import Thread

from .models import Bookmark, Rating


@login_required
def bookmark_list(request):
    bookmarks = (
        Bookmark.objects.filter(user=request.user)
        .select_related("thread", "thread__person", "thread__author")
        .order_by("-created_at")
    )
    return render(request, "engagement/bookmark_list.html", {"bookmarks": bookmarks})


@login_required
@require_POST
def bookmark_toggle(request, slug):
    thread = get_object_or_404(Thread, slug=slug, status=Thread.STATUS_PUBLISHED)
    bookmark, created = Bookmark.objects.get_or_create(user=request.user, thread=thread)
    if not created:
        bookmark.delete()
    return JsonResponse({"ok": True, "is_bookmarked": created})


@login_required
@require_POST
def rating_set(request, slug):
    thread = get_object_or_404(Thread, slug=slug, status=Thread.STATUS_PUBLISHED)
    try:
        value = int(request.POST.get("rating", "0"))
    except ValueError:
        return JsonResponse({"ok": False, "error": _("Invalid rating")}, status=400)

    if value < 1 or value > 5:
        return JsonResponse({"ok": False, "error": _("Rating must be between 1 and 5")}, status=400)

    Rating.objects.update_or_create(user=request.user, thread=thread, defaults={"value": value})
    average = thread.ratings.aggregate(avg=Avg("value")).get("avg") or 0
    return JsonResponse(
        {
            "ok": True,
            "rating": value,
            "average": round(float(average), 2),
            "badge": rating_badge(average),
        }
    )
