from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from PIL import Image

# Create your models here.
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField( default='avatar/default.jpg',upload_to='avatar')
    friends = models.ManyToManyField('self',symmetrical=False,through='Friendship',related_name='related_to',blank=True)
    display_name = models.CharField(max_length=100, unique=True)
    wins = models.IntegerField(default=0)
    losses = models.IntegerField(default=0)
    match_history = models.JSONField(default=list, blank=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if self.avatar:
            img = Image.open(self.avatar.path)
            if img.height > 300 or img.width > 300:
                output_size = (300, 300)
                img.thumbnail(output_size)
                img.save(self.avatar.path)

    def __str__(self):
        return f'{self.user.username} Profile'

class Friendship(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
    )
    from_user = models.ForeignKey('UserProfile', on_delete=models.CASCADE, related_name='friendships_sent')
    to_user = models.ForeignKey('UserProfile', on_delete=models.CASCADE, related_name='friendships_received')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = (('from_user', 'to_user'),)

    def clean(self):
        if self.from_user == self.to_user:
            raise ValidationError("You cannot add yourself as a friend.")

    def __str__(self):
        return f'{self.from_user.user.username} Friend with {self.to_user.user.username}'