from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Count
from django.shortcuts import render

from movies.models import Movie
from reviews.models import Review


@staff_member_required
def panel(request):
    top_genres = (
        Movie.objects.values("genres__name").annotate(total=Count("id")).order_by("-total")[:5]
    )
    context = {
        "movies_total": Movie.objects.count(),
        "reviews_total": Review.objects.count(),
        "top_genres": top_genres,
    }
    return render(request, "dashboard/panel.html", context)
