from django.conf import settings
from django.contrib.auth.models import User
from django.db import models

from core.validators import image_extension_validator, validate_file_size


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    display_name = models.CharField(max_length=120, blank=True)
    avatar = models.ImageField(
        upload_to="avatars/",
        blank=True,
        null=True,
        validators=[image_extension_validator, validate_file_size],
    )
    bio = models.TextField(blank=True)
    reputation = models.IntegerField(default=0)

    def __str__(self):
        return self.display_name or self.user.username


class LoginAudit(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="login_audits"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    ip_address = models.GenericIPAddressField(blank=True, null=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.user} @ {self.created_at}"
