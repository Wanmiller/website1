from django.db import models


class Person(models.Model):
    full_name = models.CharField(max_length=150)
    bio = models.TextField(blank=True)
    birth_date = models.DateField(blank=True, null=True)

    class Meta:
        ordering = ["full_name"]

    def __str__(self):
        return self.full_name


class RoleCredit(models.Model):
    ROLE_CHOICES = [
        ("actor", "Actor"),
        ("director", "Director"),
        ("writer", "Writer"),
        ("producer", "Producer"),
    ]

    movie = models.ForeignKey("movies.Movie", on_delete=models.CASCADE, related_name="credits")
    person = models.ForeignKey(Person, on_delete=models.CASCADE, related_name="credits")
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)

    class Meta:
        unique_together = ("movie", "person", "role")
        ordering = ["role", "person__full_name"]

    def __str__(self):
        return f"{self.person} as {self.role} in {self.movie}"
