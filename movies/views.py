from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.paginator import Paginator
from django.db.models import Avg, Count, Q
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, UpdateView

from .forms import MovieForm
from .models import Movie, WatchlistEvent


class StaffRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_staff


def movie_list(request):
    queryset = (
        Movie.objects.select_related("age_rating", "studio")
        .prefetch_related("genres")
        .annotate(avg_rating=Avg("reviews__rating"))
    )
    q = request.GET.get("q", "").strip()
    genre = request.GET.get("genre", "").strip()
    year = request.GET.get("year", "").strip()
    ordering = request.GET.get("ordering", "-release_year")

    if q:
        queryset = queryset.filter(Q(title__icontains=q) | Q(synopsis__icontains=q))
    if genre:
        queryset = queryset.filter(genres__slug=genre)
    if year:
        queryset = queryset.filter(release_year=year)
    if ordering in {"title", "-title", "release_year", "-release_year"}:
        queryset = queryset.order_by(ordering)

    paginator = Paginator(queryset.distinct(), 9)
    page_obj = paginator.get_page(request.GET.get("page"))

    return render(
        request,
        "movies/movie_list.html",
        {
            "page_obj": page_obj,
            "filters": {"q": q, "genre": genre, "year": year, "ordering": ordering},
        },
    )


def movie_detail(request, slug):
    movie = get_object_or_404(
        Movie.objects.select_related(
            "age_rating", "studio", "country", "language"
        ).prefetch_related("genres", "credits__person", "trailers", "reviews__user"),
        slug=slug,
    )
    if request.user.is_authenticated:
        WatchlistEvent.objects.create(user=request.user, movie=movie, action="opened_detail")
    return render(request, "movies/movie_detail.html", {"movie": movie})


class MovieCreateView(LoginRequiredMixin, StaffRequiredMixin, CreateView):
    model = Movie
    form_class = MovieForm
    template_name = "movies/movie_form.html"

    def form_valid(self, form):
        messages.success(self.request, "Movie created successfully.")
        return super().form_valid(form)


class MovieUpdateView(LoginRequiredMixin, StaffRequiredMixin, UpdateView):
    model = Movie
    slug_field = "slug"
    slug_url_kwarg = "slug"
    form_class = MovieForm
    template_name = "movies/movie_form.html"

    def form_valid(self, form):
        messages.success(self.request, "Movie updated successfully.")
        return super().form_valid(form)


class MovieDeleteView(LoginRequiredMixin, StaffRequiredMixin, DeleteView):
    model = Movie
    slug_field = "slug"
    slug_url_kwarg = "slug"
    template_name = "movies/movie_confirm_delete.html"
    success_url = reverse_lazy("movies:list")

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "Movie deleted successfully.")
        return super().delete(request, *args, **kwargs)


def movie_stats(request):
    stats = Movie.objects.values("genres__name").annotate(total=Count("id")).order_by("-total")[:10]
    return render(request, "movies/movie_stats.html", {"stats": stats})
