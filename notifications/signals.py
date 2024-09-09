from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from answers.models import Answer

from .models import Notification


@receiver(post_save, sender=Answer)
def update_answers_count(sender, instance, created, **kwargs):
    if created:
        question = instance.question
        question.answers_count = question.answer_set.count()
        question.save()

        message = f"{question.title} 有一個新回覆"

        # save the news in db
        # Prepare list of Notification instances
        notifications = [
            Notification(user=user, message=message)
            for user in question.followers.all()
        ]
        notifications.append(Notification(user=question.user, message=message))
        notifications = Notification.objects.bulk_create(notifications)

        # send the news to followers/subscribers
        channel_layer = get_channel_layer()
        group_name = f"notifications_questions_{question.id}"
        event = {
            "type": "send_notification",
            "message": message,
            "created_at": notifications[0].created_at,
        }
        async_to_sync(channel_layer.group_send)(group_name, event)


@receiver(post_delete, sender=Answer)
def update_answers_count(sender, instance, **kwargs):
    question = instance.question
    question.answer_count = question.answer_set.count()
    question.save()
