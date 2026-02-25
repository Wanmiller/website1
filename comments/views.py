from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.translation import gettext_lazy as _

from threads.models import Thread

from .forms import CommentForm
from .models import Comment


@login_required
def reply_comment(request, pk):
    parent = get_object_or_404(Comment.objects.select_related("thread"), pk=pk)
    thread = parent.thread

    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.thread = thread
            comment.parent = parent
            comment.save()
            messages.success(request, _("Reply posted."))
            return redirect("threads:detail", slug=thread.slug)
    else:
        form = CommentForm()

    return render(
        request,
        "comments/reply_form.html",
        {"form": form, "parent": parent, "thread": thread},
    )
