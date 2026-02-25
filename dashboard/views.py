from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Count
from django.shortcuts import render
from django.utils.translation import gettext_lazy as _

from comments.models import Comment
from people.models import Person
from threads.models import Thread


@staff_member_required
def panel(request):
    top_people = (
        Thread.objects.values("person__full_name").annotate(total=Count("id")).order_by("-total")[:5]
    )
    context = {
        "threads_total": Thread.objects.count(),
        "comments_total": Comment.objects.count(),
        "people_total": Person.objects.count(),
        "top_people": top_people,
        "breadcrumb_items": [
            {"label": _("Home"), "url": "/"},
            {"label": _("Dashboard"), "url": None},
        ],
    }
    return render(request, "dashboard/panel.html", context)
