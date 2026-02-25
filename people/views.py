from django.shortcuts import get_object_or_404, render

from threads.models import Thread

from .models import Person


def person_list(request):
    q = request.GET.get("q", "").strip()
    queryset = Person.objects.all()
    if q:
        queryset = queryset.filter(full_name__icontains=q)
    return render(request, "people/person_list.html", {"people": queryset, "q": q})


def person_detail(request, slug):
    person = get_object_or_404(Person, slug=slug)
    threads = Thread.objects.filter(person=person, status=Thread.STATUS_PUBLISHED).select_related(
        "author"
    )[:20]
    return render(request, "people/person_detail.html", {"person": person, "threads": threads})
