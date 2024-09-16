import random

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from faker import Faker

from teachers.models import Teacher


class Command(BaseCommand):
    help = "Generate fake data for Teacher model"

    def handle(self, *args, **kwargs):
        fake = Faker("zh_TW")
        User = get_user_model()

        programming_languages = [
            "Python",
            "JavaScript",
            "Java",
            "C++",
            "C#",
            "Ruby",
            "Go",
            "Swift",
            "Kotlin",
            "PHP",
            "R",
            "Rust",
            "TypeScript",
            "Scala",
            "Perl",
        ]

        schedules = [
            "週一上午 9:00 - 11:00",
            "週二下午 2:00 - 4:00",
            "週三上午 10:00 - 12:00",
            "週四晚上 7:00 - 9:00",
            "週五下午 3:00 - 5:00",
            "週六上午 8:00 - 10:00",
            "週日下午 1:00 - 3:00",
        ]

        introduce_templates = []

        teachers = User.objects.filter(is_teacher=True)
        for user in teachers:
            if not hasattr(user, "teacher"):
                # 隨機選擇 1 到 3 個程式語言
                selected_languages = random.sample(
                    programming_languages, random.randint(1, 3)
                )

                # 生成三個字的姓名作為 nickname
                nickname = (
                    fake.last_name() + fake.first_name()[:1] + fake.first_name()[:1]
                )

                schedule = random.choice(schedules)

                Teacher.objects.create(
                    user=user,
                    introduce=introduce,
                    nickname=nickname,
                    schedule=schedule,
                )

        self.stdout.write(
            self.style.SUCCESS("Successfully generated fake data for Teacher model")
        )
