from django.conf import settings
from django.db import models
from django.template.defaultfilters import slugify
from django.utils.translation import gettext_lazy as _


class Thread(models.Model):
    STATUS_PUBLISHED = "published"
    STATUS_HIDDEN = "hidden"
    STATUS_CHOICES = [
        (STATUS_PUBLISHED, _("Published")),
        (STATUS_HIDDEN, _("Hidden")),
    ]

    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="threads"
    )
    person = models.ForeignKey("people.Person", on_delete=models.CASCADE, related_name="threads")
    title = models.CharField(max_length=220)
    slug = models.SlugField(max_length=240, unique=True, blank=True)
    body = models.TextField()
    tags = models.ManyToManyField("engagement.Tag", through="engagement.ThreadTag", blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_PUBLISHED)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["slug"]),
            models.Index(fields=["created_at"]),
            models.Index(fields=["status"]),
        ]

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title)[:220]
            slug = base_slug or "thread"
            index = 1
            while Thread.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{index}"
                index += 1
            self.slug = slug
        super().save(*args, **kwargs)

    @property
    def score(self):
        result = self.votes.aggregate(total=models.Sum("value"))
        return int(result["total"] or 0)

    @property
    def average_rating(self):
        result = self.ratings.aggregate(avg=models.Avg("value"))
        return float(result["avg"] or 0)

    def __str__(self):
        return self.title
