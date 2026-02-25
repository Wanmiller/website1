from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST

from comments.models import Comment
from threads.models import Thread

from .models import Vote


@login_required
@require_POST
def vote_toggle(request):
    target_type = request.POST.get("target_type", "").strip()
    target_id = request.POST.get("target_id", "").strip()
    value_raw = request.POST.get("value", "1").strip()

    try:
        target_id_int = int(target_id)
        value = int(value_raw)
    except ValueError:
        return JsonResponse({"ok": False, "error": "Invalid input"}, status=400)

    if value not in (-1, 1):
        return JsonResponse({"ok": False, "error": "Value must be -1 or 1"}, status=400)

    if target_type == "thread":
        thread = Thread.objects.filter(pk=target_id_int).first()
        if not thread:
            return JsonResponse({"ok": False, "error": "Thread not found"}, status=404)
        vote, created = Vote.objects.get_or_create(
            user=request.user,
            thread=thread,
            defaults={"value": value},
        )
        if not created:
            if vote.value == value:
                vote.delete()
            else:
                vote.value = value
                vote.save()
        score = thread.score
    elif target_type == "comment":
        comment = Comment.objects.filter(pk=target_id_int).first()
        if not comment:
            return JsonResponse({"ok": False, "error": "Comment not found"}, status=404)
        vote, created = Vote.objects.get_or_create(
            user=request.user,
            comment=comment,
            defaults={"value": value},
        )
        if not created:
            if vote.value == value:
                vote.delete()
            else:
                vote.value = value
                vote.save()
        score = comment.score
    else:
        return JsonResponse({"ok": False, "error": "Invalid target_type"}, status=400)

    return JsonResponse({"ok": True, "score": score})
