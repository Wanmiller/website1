from django.http import JsonResponse
from django.shortcuts import render

from movies.models import Movie


def search_page(request):
    return render(request, "search/search_page.html")


def live_search(request):
    q = request.GET.get("q", "").strip()
    movies = Movie.objects.filter(title__icontains=q).values("title", "slug")[:8] if q else []
    return JsonResponse({"results": list(movies)})
