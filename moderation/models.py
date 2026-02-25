from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _


class Report(models.Model):
    TARGET_THREAD = "thread"
    TARGET_COMMENT = "comment"
    TARGET_CHOICES = [(TARGET_THREAD, _("Thread")), (TARGET_COMMENT, _("Comment"))]

    STATUS_OPEN = "open"
    STATUS_RESOLVED = "resolved"
    STATUS_DISMISSED = "dismissed"
    STATUS_CHOICES = [
        (STATUS_OPEN, _("Open")),
        (STATUS_RESOLVED, _("Resolved")),
        (STATUS_DISMISSED, _("Dismissed")),
    ]

    reporter = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="reports"
    )
    target_type = models.CharField(max_length=20, choices=TARGET_CHOICES)
    target_id = models.PositiveIntegerField()
    reason = models.CharField(max_length=255)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_OPEN)
    created_at = models.DateTimeField(auto_now_add=True)
    resolved_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["target_type", "target_id"]),
            models.Index(fields=["status"]),
        ]

    def __str__(self):
        return f"{self.target_type}:{self.target_id} ({self.status})"
