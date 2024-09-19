from django.core.management.base import BaseCommand
from django.utils import timezone
from faker import Faker

from users.models import User


class Command(BaseCommand):
    help = "Generate fake users data"

    def add_arguments(self, parser):
        parser.add_argument(
            "total", type=int, help="Indicates the number of users to be created"
        )

    def handle(self, *args, **kwargs):
        total = kwargs["total"]
        fake = Faker()

        for _ in range(total):
            is_student = fake.boolean()
            is_teacher = not is_student

            third_party = fake.url() if fake.boolean() else None

            user = User.objects.create_user(
                username=fake.user_name(),
                email=fake.email(),
                password="password123",
                is_student=is_student,
                is_teacher=is_teacher,
                third_party=third_party,
                name=fake.name(),
            )

            user.last_login = timezone.now()
            user.save()

            self.stdout.write(
                self.style.SUCCESS(f"Successfully created user {user.username}")
            )

        self.stdout.write(self.style.SUCCESS(f"Successfully created {total} users"))
