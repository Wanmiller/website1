from django.shortcuts import render

from movies.models import Movie


def home(request):
    featured_movies = (
        Movie.objects.select_related("age_rating", "studio")
        .prefetch_related("genres")
        .filter(is_featured=True)[:8]
    )
    latest_movies = Movie.objects.select_related("age_rating").prefetch_related("genres")[:8]
    return render(
        request,
        "core/home.html",
        {"featured_movies": featured_movies, "latest_movies": latest_movies},
    )


def about(request):
    return render(
        request,
        "core/about.html",
        {"breadcrumb_items": [{"label": "Home", "url": "/"}, {"label": "About", "url": None}]},
    )


def handler404(request, exception):
    return render(request, "core/404.html", status=404)


def handler500(request):
    return render(request, "core/500.html", status=500)
