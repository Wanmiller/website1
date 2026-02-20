from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

from genres.models import Genre
from movies.models import AgeRating, Country, Language, Movie, Studio, Tag
from people.models import Person, RoleCredit


class Command(BaseCommand):
    help = "Seed initial demo data for CineVerse"

    def handle(self, *args, **options):
        country, _ = Country.objects.get_or_create(name="Kazakhstan", code="KZ")
        lang, _ = Language.objects.get_or_create(name="Russian", code="ru")
        age, _ = AgeRating.objects.get_or_create(
            code="16+", defaults={"description": "For audiences 16+"}
        )
        studio, _ = Studio.objects.get_or_create(name="Steppe Pictures", country=country)

        genres = [
            Genre.objects.get_or_create(name="Drama", defaults={"description": "Dramatic stories"})[
                0
            ],
            Genre.objects.get_or_create(
                name="Thriller", defaults={"description": "Tense and sharp"}
            )[0],
            Genre.objects.get_or_create(name="Sci-Fi", defaults={"description": "Science fiction"})[
                0
            ],
        ]

        movie, _ = Movie.objects.get_or_create(
            title="Steppe Horizon",
            defaults={
                "synopsis": "A young director explores identity through cinema.",
                "release_year": 2025,
                "duration_minutes": 112,
                "age_rating": age,
                "studio": studio,
                "country": country,
                "language": lang,
                "is_featured": True,
            },
        )
        movie.genres.set(genres[:2])

        tag, _ = Tag.objects.get_or_create(name="festival")
        movie.tags.add(tag)

        person, _ = Person.objects.get_or_create(
            full_name="Aruzhan Bek", defaults={"bio": "Director and writer"}
        )
        RoleCredit.objects.get_or_create(movie=movie, person=person, role="director")

        if not User.objects.filter(username="staff").exists():
            User.objects.create_user(
                username="staff", password="staff12345", is_staff=True, is_superuser=True
            )

        self.stdout.write(self.style.SUCCESS("Seed completed."))
