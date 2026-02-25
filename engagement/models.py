from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.template.defaultfilters import slugify
from django.utils.translation import gettext_lazy as _

from core.validators import image_extension_validator, validate_file_size


class Tag(models.Model):
    name = models.CharField(max_length=64, unique=True)
    slug = models.SlugField(max_length=80, unique=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["name"]

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name)[:70]
            slug = base_slug or "tag"
            index = 1
            while Tag.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{index}"
                index += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class ThreadTag(models.Model):
    thread = models.ForeignKey("threads.Thread", on_delete=models.CASCADE, related_name="thread_tags")
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE, related_name="thread_tags")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [models.UniqueConstraint(fields=["thread", "tag"], name="uniq_thread_tag")]
        indexes = [models.Index(fields=["created_at"])]

    def __str__(self):
        return f"{self.thread_id}:{self.tag.name}"


class Bookmark(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="bookmarks")
    thread = models.ForeignKey("threads.Thread", on_delete=models.CASCADE, related_name="bookmarks")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["user", "thread"], name="uniq_user_thread_bookmark")
        ]
        indexes = [models.Index(fields=["created_at"])]

    def __str__(self):
        return f"{self.user} -> {self.thread}"


class Rating(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="ratings")
    thread = models.ForeignKey("threads.Thread", on_delete=models.CASCADE, related_name="ratings")
    value = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["user", "thread"], name="uniq_user_thread_rating")
        ]
        indexes = [models.Index(fields=["updated_at"])]

    def __str__(self):
        return f"{self.thread_id}={self.value}"


class Follow(models.Model):
    follower = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="person_follows",
    )
    person = models.ForeignKey("people.Person", on_delete=models.CASCADE, related_name="followers")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [models.UniqueConstraint(fields=["follower", "person"], name="uniq_follow_user_person")]
        indexes = [models.Index(fields=["created_at"])]

    def __str__(self):
        return f"{self.follower} follows {self.person}"


class Notification(models.Model):
    KIND_COMMENT = "comment"
    KIND_REPLY = "reply"
    KIND_REPORT = "report"
    KIND_CHOICES = [
        (KIND_COMMENT, _("Comment")),
        (KIND_REPLY, _("Reply")),
        (KIND_REPORT, _("Report")),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="notifications",
    )
    kind = models.CharField(max_length=20, choices=KIND_CHOICES, default=KIND_COMMENT)
    title = models.CharField(max_length=120)
    payload = models.JSONField(default=dict, blank=True)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        indexes = [models.Index(fields=["is_read", "created_at"])]

    def __str__(self):
        return f"{self.user} {self.kind}"


class Attachment(models.Model):
    thread = models.ForeignKey("threads.Thread", on_delete=models.CASCADE, related_name="attachments")
    uploaded_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="attachments",
    )
    file = models.FileField(
        upload_to="attachments/",
        validators=[image_extension_validator, validate_file_size],
    )
    alt_text = models.CharField(max_length=150, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        indexes = [models.Index(fields=["created_at"])]

    def __str__(self):
        return f"Attachment {self.pk}"


class ViewEvent(models.Model):
    thread = models.ForeignKey("threads.Thread", on_delete=models.CASCADE, related_name="view_events")
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="view_events",
    )
    session_key = models.CharField(max_length=40, blank=True)
    ip_address = models.GenericIPAddressField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        indexes = [models.Index(fields=["created_at"]), models.Index(fields=["thread", "created_at"])]

    def __str__(self):
        return f"View {self.thread_id}"
