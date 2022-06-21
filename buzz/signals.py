from django.conf import settings
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver

from .models import Profile

from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

#Your signals here
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_user_profile(sender,instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)
        # instance.profile.save()

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def save_user_profile(sender,instance, **kwargs):
    instance.profile.save()