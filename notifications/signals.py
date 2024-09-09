
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from answers.models import Answer


@receiver(post_save, sender=Answer)
def update_answers_count(sender, instance, created, **kwargs):
    if created:
        question = instance.question
        question.answers_count = question.answer_set.count()
        question.save()

        # send the news to followers/subscribers
        channel_layer = get_channel_layer()
        group_name = f"notifications_questions_{question.id}"
        event = {
            "type": "send_notification",
            "message": f"{question.title} 有一個新回覆",
        }
        async_to_sync(channel_layer.group_send)(group_name, event)

@receiver(post_delete, sender=Answer)
def update_answers_count(sender, instance, **kwargs):
    question = instance.question
    question.answer_count = question.answer_set.count()
    question.save()

@receiver(post_save, sender=Question)
def check_followers_change(sender, instance, created, **kwargs):
    pass