from typing import Any, Type
from django.db.models.base import Model
from django.db.models.signals import post_save
from django.dispatch import receiver
from loguru import logger
from django.conf import settings
from core_apps.user_profile.models import Profile


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_user_profile(sender: Type[Model], instance: Model, created: bool, **kwargs: Any):
    if created:
        Profile.objects.create(user=instance)
        print(type(instance), instance.__class__.__name__)
        logger.info(f"Profile created for {instance.first_name} {instance.last_name}")

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def save_user_profile(sender: Type[Model], instance: Model, **kwargs: Any) -> None:
    instance.profile.save()