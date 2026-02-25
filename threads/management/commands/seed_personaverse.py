import random

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

from comments.models import Comment
from engagement.models import Bookmark, Follow, Notification, Rating, Tag, ThreadTag, ViewEvent
from moderation.models import Report
from people.models import Person
from threads.models import Thread
from votes.models import Vote


class Command(BaseCommand):
    help = "Seed PersonaVerse demo data (people, threads, comments, votes, bookmarks, ratings)"

    def handle(self, *args, **options):
        staff, _ = User.objects.get_or_create(username="staff", defaults={"is_staff": True, "is_superuser": True})
        staff.set_password("staff12345")
        staff.save()

        users = [staff]
        for i in range(1, 6):
            user, _ = User.objects.get_or_create(username=f"pv_user_{i}", defaults={"email": f"pv{i}@local"})
            user.set_password("test12345")
            user.save()
            users.append(user)

        people_data = [
            ("Elon Musk", "Tech entrepreneur and public figure", True),
            ("Taylor Swift", "Singer-songwriter and performer", True),
            ("Cristiano Ronaldo", "Professional football player", True),
            ("MrBeast", "YouTube creator and philanthropist", True),
            ("Emma Watson", "Actor and activist", True),
            ("Keanu Reeves", "Actor known for humble public persona", True),
            ("Sam Altman", "Tech executive in AI space", True),
            ("Zendaya", "Actor and producer", True),
        ]

        people = []
        for full_name, bio, verified in people_data:
            person, _ = Person.objects.get_or_create(
                full_name=full_name,
                defaults={"bio": bio, "is_verified": verified},
            )
            person.bio = bio
            person.is_verified = verified
            person.save()
            people.append(person)

        thread_titles = [
            "What do you think about recent interviews?",
            "Most underrated projects in their career",
            "Public image vs reality discussion",
            "Best long-form content to understand this person",
            "How media coverage changed over the years",
            "What can creators learn from this profile?",
            "Most controversial moment: fair criticism?",
            "Community takes: hot or not",
            "Do you agree with their latest decisions?",
            "Long-term impact on culture and audience",
        ]

        rng = random.Random(42)
        threads = []
        tags = [
            Tag.objects.get_or_create(name=name)[0]
            for name in ("news", "analysis", "career", "controversy", "timeline", "media")
        ]
        for idx in range(24):
            person = people[idx % len(people)]
            author = users[(idx % (len(users) - 1)) + 1]
            title = f"{person.full_name}: {thread_titles[idx % len(thread_titles)]}"
            body = (
                "Share your analysis, sources, and respectful opinions. "
                "This thread is for constructive discussion around profile, work, and public impact."
            )
            thread, _ = Thread.objects.get_or_create(
                title=title,
                person=person,
                defaults={"author": author, "body": body},
            )
            thread.author = author
            thread.body = body
            thread.status = Thread.STATUS_PUBLISHED
            thread.save()
            ThreadTag.objects.get_or_create(thread=thread, tag=tags[idx % len(tags)])
            ThreadTag.objects.get_or_create(thread=thread, tag=tags[(idx + 1) % len(tags)])
            threads.append(thread)

        for idx, thread in enumerate(threads):
            base_user = users[(idx % (len(users) - 1)) + 1]
            comment, _ = Comment.objects.get_or_create(
                thread=thread,
                author=base_user,
                parent=None,
                defaults={
                    "body": "Interesting angle. I think context and timeline matter a lot here.",
                    "status": Comment.STATUS_PUBLISHED,
                },
            )
            reply_user = users[((idx + 1) % (len(users) - 1)) + 1]
            Comment.objects.get_or_create(
                thread=thread,
                author=reply_user,
                parent=comment,
                defaults={
                    "body": "Agree on context. Would also compare audience reaction across platforms.",
                    "status": Comment.STATUS_PUBLISHED,
                },
            )

            for voter in users[1:]:
                vote_value = 1 if rng.random() > 0.3 else -1
                Vote.objects.update_or_create(
                    user=voter,
                    thread=thread,
                    comment=None,
                    defaults={"value": vote_value},
                )
                Rating.objects.update_or_create(
                    user=voter,
                    thread=thread,
                    defaults={"value": rng.randint(3, 5)},
                )
                if rng.random() > 0.55:
                    Bookmark.objects.get_or_create(user=voter, thread=thread)

            ViewEvent.objects.get_or_create(
                thread=thread,
                user=base_user,
                session_key=f"seed-{thread.id}",
                defaults={"ip_address": "127.0.0.1"},
            )

        for idx, person in enumerate(people):
            Follow.objects.get_or_create(follower=users[(idx % 5) + 1], person=person)
            Notification.objects.get_or_create(
                user=users[(idx % 5) + 1],
                kind=Notification.KIND_COMMENT,
                title=f"New discussion about {person.full_name}",
                defaults={"payload": {"person_id": person.id}},
            )

        # Create a couple of open reports for moderation demo.
        if threads:
            Report.objects.get_or_create(
                reporter=users[1],
                target_type=Report.TARGET_THREAD,
                target_id=threads[0].id,
                defaults={"reason": "Potential misinformation in claims"},
            )
            first_comment = Comment.objects.first()
            if first_comment:
                Report.objects.get_or_create(
                    reporter=users[2],
                    target_type=Report.TARGET_COMMENT,
                    target_id=first_comment.id,
                    defaults={"reason": "Personal attack tone"},
                )

        self.stdout.write(self.style.SUCCESS("PersonaVerse seed completed."))
