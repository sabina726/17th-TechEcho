from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from answers.models import Answer

from .models import Notification


@receiver(post_save, sender=Answer, weak=False)
def update_answers_count(sender, instance, created, **kwargs):
    if created:
        question = instance.question
        question.answers_count = question.answer_set.count()
        question.save()

        message = f"{question.title} 有一個新回覆"
        url_name = "questions:show"
        question_id = question.id
        answer_id = instance.id

        notifications = [
            Notification(
                user=user,
                question_id=question_id,
                answer_id=answer_id,
                message=message,
                url_name=url_name,
            )
            for user in question.followers.all()
            if user != instance.user
        ]
        if question.user != instance.user:
            notifications.append(
                Notification(
                    user=question.user,
                    question_id=question_id,
                    answer_id=answer_id,
                    message=message,
                    url_name=url_name,
                )
            )
        if len(notifications) == 0:
            return

        notifications = Notification.objects.bulk_create(notifications)

        channel_layer = get_channel_layer()
        group_name = f"notifications_questions_{question.id}"
        event = {
            "type": "send_notification",
            "message": message,
            "url_name": url_name,
            "question_id": question_id,
            "answer_id": answer_id,
        }
        async_to_sync(channel_layer.group_send)(group_name, event)


@receiver(post_delete, sender=Answer, weak=False)
def update_answers_count(sender, instance, **kwargs):
    question = instance.question
    question.answer_count = question.answer_set.count()
    question.save()
