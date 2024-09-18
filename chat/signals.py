from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from reservations.models import StudentReservation
from .models import ChatGroup


@receiver(post_save, sender=StudentReservation)
def create_chat_group(_, instance, created):
    if created:
        group_name = f"chat_group_${instance.id}"
        new_chat_group = ChatGroup.objects.create(group_name=group_name, reservation=instance)
        members = [
            instance.student,
            instance.schedule.teacher
        ]
        new_chat_group.members.add(*members)
        
