from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Status


User = get_user_model()


@receiver(post_save, sender=User)
def create_status(instance, created, **kwargs):
    if not created:
        return

    Status.objects.create(user=instance)
