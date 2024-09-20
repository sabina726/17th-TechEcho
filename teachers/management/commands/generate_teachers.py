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

        schedules = [
            "週一上午 9:00 - 11:00",
            "週二下午 2:00 - 4:00",
            "週三上午 10:00 - 12:00",
            "週四晚上 7:00 - 9:00",
            "週五下午 3:00 - 5:00",
            "週六上午 8:00 - 10:00",
            "週日下午 1:00 - 3:00",
        ]

        introduce_templates = [
            """劉向曾經提到過，君子居人間則治，小人居人間則亂。君子慾和人，
            譬猶水火不相能然也，而鼎在其間，水火不亂，乃和百味，是以君子不可
            不慎擇人在其間。希望大家實際感受一下這段話。李白曾提出，天生我材
            必有用。這句話反映了問題的急切性。不難發現，問題在於該用什麼標準
            來做決定呢？約翰遜講過，失望雖然常常發生，但總沒有絕望那麼可怕。
            希望大家能發現話中之話。德謨克里特曾經提到過，連一個高尚朋友都沒
            有的人，是不值得活的。這啟發了我。蘇格拉底曾經提過，美色不常駐。
            帶著這句話，我們還要更加慎重的審視這個問題。如果仔細思考老師介紹
            ，會發現其中蘊含的深遠意義。"""
        ]

        teachers = User.objects.filter(is_teacher=True)
        for user in teachers:
            if not hasattr(user, "teacher"):

                schedule = random.choice(schedules)

                Teacher.objects.create(
                    user=user,
                    introduce=introduce_templates,
                    schedule=schedule,
                )

        self.stdout.write(
            self.style.SUCCESS("Successfully generated fake data for Teacher model")
        )
