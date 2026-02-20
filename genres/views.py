from django.shortcuts import get_object_or_404, render

from .models import Genre


def genre_list(request):
    genres = Genre.objects.all()
    return render(request, "genres/genre_list.html", {"genres": genres})


def genre_detail(request, slug):
    genre = get_object_or_404(Genre.objects.prefetch_related("movies"), slug=slug)
    return render(request, "genres/genre_detail.html", {"genre": genre})
