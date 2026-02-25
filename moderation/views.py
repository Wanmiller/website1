from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.views.decorators.http import require_POST

from comments.models import Comment
from threads.models import Thread

from .models import Report


@staff_member_required
def panel(request):
    open_reports = Report.objects.filter(status=Report.STATUS_OPEN)
    resolved_reports = Report.objects.exclude(status=Report.STATUS_OPEN)[:50]
    return render(
        request,
        "moderation/panel.html",
        {
            "open_reports": open_reports,
            "resolved_reports": resolved_reports,
            "breadcrumb_items": [
                {"label": _("Home"), "url": "/"},
                {"label": _("Moderation"), "url": None},
            ],
        },
    )


@staff_member_required
@require_POST
def report_action(request, report_id):
    report = get_object_or_404(Report, pk=report_id)
    action = request.POST.get("action", "").strip()

    if report.target_type == Report.TARGET_THREAD:
        target = Thread.objects.filter(pk=report.target_id).first()
    else:
        target = Comment.objects.filter(pk=report.target_id).first()

    if action == "hide" and target:
        target.status = "hidden"
        target.save(update_fields=["status"])
        report.status = Report.STATUS_RESOLVED
    elif action == "publish" and target:
        target.status = "published"
        target.save(update_fields=["status"])
        report.status = Report.STATUS_RESOLVED
    elif action == "dismiss":
        report.status = Report.STATUS_DISMISSED
    else:
        messages.error(request, _("Invalid action."))
        return redirect("moderation:panel")

    report.resolved_at = timezone.now()
    report.save(update_fields=["status", "resolved_at"])
    messages.success(request, _("Moderation action applied."))
    return redirect("moderation:panel")


@login_required
@require_POST
def create_report(request):
    target_type = request.POST.get("target_type", "").strip()
    target_id = request.POST.get("target_id", "").strip()
    reason = request.POST.get("reason", "").strip()[:255]

    try:
        target_id_int = int(target_id)
    except ValueError:
        messages.error(request, _("Invalid report target."))
        return redirect(request.POST.get("next") or "core:home")

    if target_type not in {Report.TARGET_THREAD, Report.TARGET_COMMENT} or not reason:
        messages.error(request, _("Invalid report payload."))
        return redirect(request.POST.get("next") or "core:home")

    Report.objects.create(
        reporter=request.user,
        target_type=target_type,
        target_id=target_id_int,
        reason=reason,
    )
    messages.success(request, _("Report submitted."))
    return redirect(request.POST.get("next") or "core:home")
