from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class UserVerification(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_verified = models.BooleanField(default=False)

# Automatically create UserVerification when a User is created
@receiver(post_save, sender=User)
def create_user_verification(sender, instance, created, **kwargs):
    if created:
        UserVerification.objects.create(user=instance)
