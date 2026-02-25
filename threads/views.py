from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Count, IntegerField, Q, Sum, Value
from django.db.models.functions import Coalesce
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.dateparse import parse_date
from django.utils.translation import gettext_lazy as _

from comments.forms import CommentForm
from comments.models import Comment
from engagement.models import Bookmark, Rating, ViewEvent
from people.models import Person

from .forms import ThreadForm
from .models import Thread


def _user_can_manage_thread(user, thread):
    if not user.is_authenticated:
        return False
    return user.is_staff or thread.author_id == user.id


def _apply_ordering(queryset, ordering: str):
    if ordering == "top":
        return queryset.order_by("-vote_score", "-created_at")
    if ordering == "hot":
        return queryset.annotate(
            comments_count=Count("comments"),
        ).order_by("-vote_score", "-comments_count", "-created_at")
    return queryset.order_by("-created_at")


def thread_list(request):
    q = request.GET.get("q", "").strip()
    person_slug = request.GET.get("person", "").strip()
    ordering = request.GET.get("ordering", "hot").strip() or "hot"
    created_after = request.GET.get("created_after", "").strip()
    score_min = request.GET.get("score_min", "").strip()

    queryset = (
        Thread.objects.select_related("author", "person")
        .filter(status=Thread.STATUS_PUBLISHED)
        .annotate(vote_score=Coalesce(Sum("votes__value"), Value(0), output_field=IntegerField()))
    )

    if q:
        queryset = queryset.filter(Q(title__icontains=q) | Q(body__icontains=q))
    if person_slug:
        queryset = queryset.filter(person__slug=person_slug)
    if created_after:
        date_value = parse_date(created_after)
        if date_value:
            queryset = queryset.filter(created_at__date__gte=date_value)
    if score_min:
        try:
            queryset = queryset.filter(vote_score__gte=int(score_min))
        except ValueError:
            pass

    queryset = _apply_ordering(queryset, ordering)

    paginator = Paginator(queryset, 10)
    page_obj = paginator.get_page(request.GET.get("page", 1))

    persons = Person.objects.all()[:100]
    return render(
        request,
        "threads/thread_list.html",
        {
            "page_obj": page_obj,
            "persons": persons,
            "filters": {
                "q": q,
                "person": person_slug,
                "ordering": ordering,
                "created_after": created_after,
                "score_min": score_min,
            },
        },
    )


def thread_detail(request, slug):
    thread = get_object_or_404(
        Thread.objects.select_related("author", "person").filter(status=Thread.STATUS_PUBLISHED),
        slug=slug,
    )
    comments = thread.comments.select_related("author").filter(status=Comment.STATUS_PUBLISHED)
    if request.user.is_authenticated:
        user = request.user
    else:
        user = None
    ViewEvent.objects.create(
        thread=thread,
        user=user,
        session_key=request.session.session_key or "",
        ip_address=request.META.get("REMOTE_ADDR"),
    )

    is_bookmarked = False
    user_rating = None
    if request.user.is_authenticated:
        is_bookmarked = Bookmark.objects.filter(user=request.user, thread=thread).exists()
        user_rating = Rating.objects.filter(user=request.user, thread=thread).first()

    comment_form = CommentForm()
    return render(
        request,
        "threads/thread_detail.html",
        {
            "thread": thread,
            "comments": comments,
            "comment_form": comment_form,
            "is_bookmarked": is_bookmarked,
            "user_rating": user_rating,
            "rating_values": [1, 2, 3, 4, 5],
            "can_manage_thread": _user_can_manage_thread(request.user, thread),
            "breadcrumb_items": [
                {"label": _("Home"), "url": "/"},
                {"label": _("Threads"), "url": "/threads/"},
                {"label": thread.title, "url": None},
            ],
        },
    )


@login_required
def thread_create(request):
    person_id = request.GET.get("person")
    if request.method == "POST":
        form = ThreadForm(request.POST)
        if form.is_valid():
            thread = form.save(commit=False)
            thread.author = request.user
            thread.save()
            messages.success(request, _("Thread created."))
            return redirect("threads:detail", slug=thread.slug)
    else:
        initial = {"person": person_id} if person_id else None
        form = ThreadForm(initial=initial)
    return render(
        request,
        "threads/thread_form.html",
        {
            "form": form,
            "is_edit": False,
            "breadcrumb_items": [
                {"label": _("Home"), "url": "/"},
                {"label": _("Threads"), "url": "/threads/"},
                {"label": _("Create"), "url": None},
            ],
        },
    )


@login_required
def thread_update(request, slug):
    thread = get_object_or_404(Thread.objects.select_related("author", "person"), slug=slug)
    if not _user_can_manage_thread(request.user, thread):
        messages.error(request, _("You do not have permission to edit this thread."))
        return redirect("threads:detail", slug=thread.slug)

    if request.method == "POST":
        form = ThreadForm(request.POST, instance=thread)
        if form.is_valid():
            form.save()
            messages.success(request, _("Thread updated."))
            return redirect("threads:detail", slug=thread.slug)
    else:
        form = ThreadForm(instance=thread)

    return render(
        request,
        "threads/thread_form.html",
        {
            "form": form,
            "thread": thread,
            "is_edit": True,
            "breadcrumb_items": [
                {"label": _("Home"), "url": "/"},
                {"label": _("Threads"), "url": "/threads/"},
                {"label": thread.title, "url": f"/threads/{thread.slug}/"},
                {"label": _("Edit"), "url": None},
            ],
        },
    )


@login_required
def thread_delete(request, slug):
    thread = get_object_or_404(Thread.objects.select_related("author", "person"), slug=slug)
    if not _user_can_manage_thread(request.user, thread):
        messages.error(request, _("You do not have permission to delete this thread."))
        return redirect("threads:detail", slug=thread.slug)

    if request.method == "POST":
        thread.delete()
        messages.success(request, _("Thread deleted."))
        return redirect("threads:list")

    return render(
        request,
        "threads/thread_confirm_delete.html",
        {
            "thread": thread,
            "breadcrumb_items": [
                {"label": _("Home"), "url": "/"},
                {"label": _("Threads"), "url": "/threads/"},
                {"label": thread.title, "url": f"/threads/{thread.slug}/"},
                {"label": _("Delete"), "url": None},
            ],
        },
    )


@login_required
def thread_comment_create(request, slug):
    thread = get_object_or_404(Thread, slug=slug, status=Thread.STATUS_PUBLISHED)
    if request.method != "POST":
        return redirect("threads:detail", slug=slug)

    form = CommentForm(request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.author = request.user
        comment.thread = thread
        comment.save()
        messages.success(request, _("Comment posted."))
    else:
        messages.error(request, _("Comment is invalid."))

    return redirect("threads:detail", slug=slug)
