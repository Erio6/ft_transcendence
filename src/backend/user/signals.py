from django.db.models.signals import post_save # This is a signal that gets fired after an object is saved (the user)
from django.contrib.auth.models import User # This is the user model that we want to create a profile for
from django.dispatch import receiver # This is a decorator that will receive the signal
from .models import UserProfile
from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.dispatch import receiver


@receiver(user_logged_in)
def user_logged_in_handler(sender, request, user, **kwargs):
    user.userprofile.is_online = True
    user.userprofile.save()

@receiver(user_logged_out)
def user_logged_out_handler(sender, request, user, **kwargs):
    user.userprofile.is_online = False
    user.userprofile.save()

@receiver(post_save, sender=User) # When a user is saved, send this signal
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance, display_name=instance.username)

@receiver(post_save, sender=User) # When a user is saved, send this signal
def save_user_profile(sender, instance, **kwargs):
    instance.userprofile.save()

