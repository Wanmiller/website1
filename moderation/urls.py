from django.urls import path

from .views import create_report, panel, report_action

urlpatterns = [
    path("", panel, name="panel"),
    path("report/create/", create_report, name="create_report"),
    path("report/<int:report_id>/action/", report_action, name="report_action"),
]
