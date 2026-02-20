from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render

from movies.models import Movie

from .models import Favorite


@login_required
def favorites_list(request):
    favorites = Favorite.objects.filter(user=request.user).select_related("movie")
    return render(request, "favorites/favorites_list.html", {"favorites": favorites})


@login_required
def toggle_favorite(request, slug):
    movie = get_object_or_404(Movie, slug=slug)
    favorite, created = Favorite.objects.get_or_create(user=request.user, movie=movie)
    if not created:
        favorite.delete()
    return redirect("movies:detail", slug=slug)


@login_required
def toggle_favorite_ajax(request, slug):
    if request.method != "POST":
        return JsonResponse({"error": "Method not allowed"}, status=405)
    movie = get_object_or_404(Movie, slug=slug)
    favorite, created = Favorite.objects.get_or_create(user=request.user, movie=movie)
    state = True
    if not created:
        favorite.delete()
        state = False
    return JsonResponse({"ok": True, "is_favorite": state})
