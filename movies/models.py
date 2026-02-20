from django.core.validators import FileExtensionValidator, MaxValueValidator, MinValueValidator
from django.db import models
from django.template.defaultfilters import slugify
from django.urls import reverse


class Country(models.Model):
    name = models.CharField(max_length=100, unique=True)
    code = models.CharField(max_length=3, unique=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Language(models.Model):
    name = models.CharField(max_length=100, unique=True)
    code = models.CharField(max_length=8, unique=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class AgeRating(models.Model):
    code = models.CharField(max_length=10, unique=True)
    description = models.CharField(max_length=255)

    class Meta:
        ordering = ["code"]

    def __str__(self):
        return self.code


class Studio(models.Model):
    name = models.CharField(max_length=150, unique=True)
    country = models.ForeignKey(Country, on_delete=models.PROTECT, related_name="studios")

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Movie(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220, unique=True, blank=True)
    synopsis = models.TextField()
    release_year = models.PositiveIntegerField(
        validators=[MinValueValidator(1900), MaxValueValidator(2100)]
    )
    duration_minutes = models.PositiveIntegerField(default=90)
    age_rating = models.ForeignKey(AgeRating, on_delete=models.PROTECT, related_name="movies")
    studio = models.ForeignKey(Studio, on_delete=models.PROTECT, related_name="movies")
    country = models.ForeignKey(Country, on_delete=models.PROTECT, related_name="movies")
    language = models.ForeignKey(Language, on_delete=models.PROTECT, related_name="movies")
    genres = models.ManyToManyField("genres.Genre", related_name="movies", blank=True)
    tags = models.ManyToManyField(
        "movies.Tag", through="MovieTag", related_name="movies", blank=True
    )
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-release_year", "title"]
        indexes = [
            models.Index(fields=["title"]),
            models.Index(fields=["release_year"]),
            models.Index(fields=["slug"]),
        ]

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title)
            slug = base_slug
            index = 1
            while Movie.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{index}"
                index += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("movies:detail", kwargs={"slug": self.slug})

    @property
    def average_rating(self):
        result = self.reviews.aggregate(avg=models.Avg("rating"))
        return round(result["avg"] or 0, 2)


class MovieImage(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(
        upload_to="movies/images/",
        validators=[FileExtensionValidator(["jpg", "jpeg", "png", "webp"])],
        blank=True,
        null=True,
    )
    alt_text = models.CharField(max_length=200, default="Movie cover")
    is_primary = models.BooleanField(default=False)

    class Meta:
        ordering = ["-is_primary"]

    def __str__(self):
        return f"Image for {self.movie.title}"


class Trailer(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name="trailers")
    title = models.CharField(max_length=200)
    url = models.URLField()

    class Meta:
        ordering = ["title"]

    def __str__(self):
        return self.title


class Tag(models.Model):
    name = models.CharField(max_length=80, unique=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True)

    class Meta:
        ordering = ["name"]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class MovieTag(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)

    class Meta:
        unique_together = ("movie", "tag")

    def __str__(self):
        return f"{self.movie} - {self.tag}"


class WatchlistEvent(models.Model):
    user = models.ForeignKey("auth.User", on_delete=models.CASCADE, related_name="watchlist_events")
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name="watchlist_events")
    action = models.CharField(max_length=50, default="viewed")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.user} {self.action} {self.movie}"
