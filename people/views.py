from django.shortcuts import get_object_or_404, render

from .models import Person


def person_list(request):
    people = Person.objects.all()
    return render(request, "people/person_list.html", {"people": people})


def person_detail(request, pk):
    person = get_object_or_404(Person.objects.prefetch_related("credits__movie"), pk=pk)
    return render(request, "people/person_detail.html", {"person": person})
