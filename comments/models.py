from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _


class Comment(models.Model):
    STATUS_PUBLISHED = "published"
    STATUS_HIDDEN = "hidden"
    STATUS_CHOICES = [
        (STATUS_PUBLISHED, _("Published")),
        (STATUS_HIDDEN, _("Hidden")),
    ]

    thread = models.ForeignKey("threads.Thread", on_delete=models.CASCADE, related_name="comments")
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="comments"
    )
    parent = models.ForeignKey(
        "self", on_delete=models.CASCADE, null=True, blank=True, related_name="replies"
    )
    body = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_PUBLISHED)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["created_at"]
        indexes = [models.Index(fields=["created_at"]), models.Index(fields=["status"])]

    @property
    def score(self):
        result = self.votes.aggregate(total=models.Sum("value"))
        return int(result["total"] or 0)

    def __str__(self):
        return f"Comment by {self.author} on {self.thread}"
