from django.http import JsonResponse
from django.shortcuts import render
from django.utils.translation import gettext as _

from people.models import Person
from threads.models import Thread


def search_page(request):
    q = request.GET.get("q", "").strip()
    threads = []
    people = []
    if q:
        threads = (
            Thread.objects.filter(status=Thread.STATUS_PUBLISHED, title__icontains=q)
            .select_related("person", "author")
            .order_by("-created_at")[:20]
        )
        people = Person.objects.filter(full_name__icontains=q).order_by("full_name")[:20]

    return render(
        request,
        "search/search_page.html",
        {
            "q": q,
            "threads": threads,
            "people": people,
        },
    )


def live_search(request):
    q = request.GET.get("q", "").strip()
    if not q:
        return JsonResponse({"results": []})

    person_rows = Person.objects.filter(full_name__icontains=q).values("full_name", "slug")[:4]
    thread_rows = (
        Thread.objects.filter(status=Thread.STATUS_PUBLISHED, title__icontains=q)
        .values("title", "slug")[:6]
    )

    results = []
    for item in person_rows:
        results.append(
            {
                "kind": "person",
                "title": item["full_name"],
                "subtitle": _("Person"),
                "url": f"/people/{item['slug']}/",
            }
        )
    for item in thread_rows:
        results.append(
            {
                "kind": "thread",
                "title": item["title"],
                "subtitle": _("Thread"),
                "url": f"/threads/{item['slug']}/",
            }
        )
    return JsonResponse({"results": results})
