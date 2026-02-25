from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models import Q


class Vote(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="votes")
    thread = models.ForeignKey(
        "threads.Thread", on_delete=models.CASCADE, null=True, blank=True, related_name="votes"
    )
    comment = models.ForeignKey(
        "comments.Comment", on_delete=models.CASCADE, null=True, blank=True, related_name="votes"
    )
    value = models.SmallIntegerField(validators=[MinValueValidator(-1), MaxValueValidator(1)])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.CheckConstraint(
                condition=(
                    Q(thread__isnull=False, comment__isnull=True)
                    | Q(thread__isnull=True, comment__isnull=False)
                ),
                name="vote_single_target",
            ),
            models.UniqueConstraint(fields=["user", "thread"], name="vote_unique_user_thread"),
            models.UniqueConstraint(fields=["user", "comment"], name="vote_unique_user_comment"),
        ]
        indexes = [models.Index(fields=["created_at"])]

    def __str__(self):
        target = self.thread_id or self.comment_id
        return f"{self.user} {self.value} -> {target}"
