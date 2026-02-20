from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render

from movies.models import Movie

from .forms import ReviewForm
from .models import Review


def review_list(request):
    reviews = Review.objects.select_related("movie", "user")
    return render(request, "reviews/review_list.html", {"reviews": reviews})


@login_required
def my_reviews(request):
    reviews = Review.objects.filter(user=request.user).select_related("movie")
    return render(request, "reviews/my_reviews.html", {"reviews": reviews})


@login_required
def review_create(request):
    if request.method == "POST":
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.save()
            messages.success(request, "Review submitted.")
            return redirect("reviews:my_reviews")
    else:
        form = ReviewForm()
    return render(request, "reviews/review_form.html", {"form": form})


@login_required
def review_ajax_rate(request, movie_id):
    if request.method != "POST":
        return JsonResponse({"error": "Method not allowed"}, status=405)

    movie = get_object_or_404(Movie, pk=movie_id)
    rating = int(request.POST.get("rating", 0))
    if rating < 1 or rating > 5:
        return JsonResponse({"error": "Rating must be 1-5"}, status=400)

    review, created = Review.objects.get_or_create(
        user=request.user,
        movie=movie,
        defaults={
            "title": f"Rating for {movie.title}",
            "body": "Quick rating from AJAX.",
            "rating": rating,
        },
    )
    if not created:
        review.rating = rating
        review.save(update_fields=["rating", "updated_at"])

    return JsonResponse({"ok": True, "rating": review.rating, "average": movie.average_rating})
