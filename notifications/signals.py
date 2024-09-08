from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.db.models.signals import post_save
from django.dispatch import receiver

from answers.models import Answer


@receiver(post_save, sender=Answer)
def update_answers_count(sender, instance, created, **kwargs):
    if created:
        question = instance.question
        question.answers_count = question.answer_set.count()
        question.save()

        channel_layer = get_channel_layer()
        group_name = "notifications"
        event = {
            "type": "send_notification",
            "message": f"您追蹤的問題 {question.title} 有一個新回覆",
        }
        async_to_sync(channel_layer.group_send)(group_name, event)
