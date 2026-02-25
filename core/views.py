from django.db.models import Count, IntegerField, Q, Sum, Value
from django.db.models.functions import Coalesce
from django.shortcuts import render
from django.utils.translation import gettext_lazy as _

from comments.models import Comment
from people.models import Person
from threads.models import Thread


def home(request):
    ordering = (request.GET.get("ordering", "hot").strip() or "hot").lower()
    if ordering not in {"hot", "new", "top"}:
        ordering = "hot"

    published_threads = (
        Thread.objects.select_related("author", "person")
        .filter(status=Thread.STATUS_PUBLISHED)
        .annotate(
            vote_score=Coalesce(Sum("votes__value"), Value(0), output_field=IntegerField()),
            comments_count=Count(
                "comments",
                filter=Q(comments__status=Comment.STATUS_PUBLISHED),
                distinct=True,
            ),
        )
    )

    if ordering == "new":
        ordered_threads = published_threads.order_by("-created_at")
    elif ordering == "top":
        ordered_threads = published_threads.order_by("-vote_score", "-created_at")
    else:
        ordered_threads = published_threads.order_by("-vote_score", "-comments_count", "-created_at")

    ordered_slice = list(ordered_threads[:7])
    hero_thread = ordered_slice[0] if ordered_slice else None
    trending_threads = ordered_slice[1:] if hero_thread else []

    fresh_threads = list(
        published_threads.order_by("-created_at").select_related("author", "person")[:5]
    )

    spotlight_people = (
        Person.objects.filter(threads__status=Thread.STATUS_PUBLISHED)
        .annotate(
            thread_count=Count(
                "threads",
                filter=Q(threads__status=Thread.STATUS_PUBLISHED),
                distinct=True,
            )
        )
        .order_by("-thread_count", "full_name")[:6]
    )

    stats = {
        "total_threads": Thread.objects.filter(status=Thread.STATUS_PUBLISHED).count(),
        "total_comments": Comment.objects.filter(
            status=Comment.STATUS_PUBLISHED,
            thread__status=Thread.STATUS_PUBLISHED,
        ).count(),
        "total_people": Person.objects.count(),
    }

    return render(
        request,
        "core/home.html",
        {
            "ordering": ordering,
            "hero_thread": hero_thread,
            "trending_threads": trending_threads,
            "fresh_threads": fresh_threads,
            "spotlight_people": spotlight_people,
            "stats": stats,
        },
    )


def about(request):
    return render(
        request,
        "core/about.html",
        {"breadcrumb_items": [{"label": _("Home"), "url": "/"}, {"label": _("About"), "url": None}]},
    )


def handler404(request, exception):
    return render(request, "core/404.html", status=404)


def handler500(request):
    return render(request, "core/500.html", status=500)
