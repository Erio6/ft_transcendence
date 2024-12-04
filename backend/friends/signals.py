from django.db.models.signals import post_save # This is a signal that gets fired after an object is saved (the user)
from django.dispatch import receiver # This is a decorator that will receive the signal
from .models import  FriendList
from django.contrib.auth.models import User

@receiver(post_save, sender=User)
def create_friendlist(sender, instance, created, **kwargs):
    if created:
        FriendList.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_friendlist(sender, instance, **kwargs):
    instance.friend_list.save()