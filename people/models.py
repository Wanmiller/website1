from django.db import models
from django.template.defaultfilters import slugify

from core.validators import image_extension_validator, validate_file_size


class Person(models.Model):
    full_name = models.CharField(max_length=150)
    slug = models.SlugField(max_length=180, unique=True, blank=True, null=True)
    bio = models.TextField(blank=True)
    avatar = models.ImageField(
        upload_to="people/avatars/",
        blank=True,
        null=True,
        validators=[image_extension_validator, validate_file_size],
    )
    is_verified = models.BooleanField(default=False)
    birth_date = models.DateField(blank=True, null=True)

    class Meta:
        ordering = ["full_name"]

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.full_name)[:160]
            slug = base_slug or "person"
            index = 1
            while Person.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{index}"
                index += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        return self.full_name
