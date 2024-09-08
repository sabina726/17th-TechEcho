from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync    
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
            "type": "send_model_notification",
            'message': f'new answers count of {question.title} is {question.answers_count}'
        }
        async_to_sync(channel_layer.group_send)(group_name, event)