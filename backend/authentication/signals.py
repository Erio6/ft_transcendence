from django.db.models.signals import post_save # This is a signal that gets fired after an object is saved (the user)
from django.contrib.auth.models import User # This is the user model that we want to create a profile for
from django.dispatch import receiver # This is a decorator that will receive the signal
from .models import UserProfile

@receiver(post_save, sender=User) # When a user is saved, send this signal
def create_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User) # When a user is saved, send this signal
def save_profile(sender, instance, **kwargs):
    instance.userprofile.save()