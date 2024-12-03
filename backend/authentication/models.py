import os.path
from django.db import models
from django.contrib.auth.models import User
from PIL import Image

# Create your models here.
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField( default='avatar/default.jpg',upload_to='avatar')
    display_name = models.CharField(max_length=100, unique=True)
    wins = models.IntegerField(default=0)
    losses = models.IntegerField(default=0)
    match_history = models.JSONField(default=list, blank=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if self.avatar and os.path.exists(self.avatar.path):
            img = Image.open(self.avatar.path)
            if img.height > 300 or img.width > 300:
                output_size = (300, 300)
                img.thumbnail(output_size)
                img.save(self.avatar.path)

    def __str__(self):
        return f'{self.user.username} Profile'

class FriendList(models.Model):
    user_profile = models.OneToOneField(UserProfile, on_delete=models.CASCADE, related_name='friend_list')
    friends = models.ManyToManyField(UserProfile, blank=True, related_name='friends')

    def __str__(self):
        return self.user_profile.user.username

    def add_friend(self, account):
        if not account in self.friends.all():
            self.friends.add(account)

    def remove_friend(self, account):
        if account in self.friends.all():
            self.friends.remove(account)

    def unfriend(self, removee):
        remover_friends_list = self
        remover_friends_list.remove_friend(removee)
        friends_list = FriendList.objects.get(user=removee)
        friends_list.remove_friend(self.user_profile)

    def is_mutual_friend(self,friend):
        if friend in self.friends.all():
            return True

class FriendRequest(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('declined', 'Declined')
    )
    sender = models.ForeignKey(UserProfile, related_name='sender', on_delete=models.CASCADE)
    receiver = models.ForeignKey(UserProfile, related_name='receiver', on_delete=models.CASCADE)
    status = models.CharField(choices=STATUS_CHOICES, default='Pending')
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"From {self.sender.user.username} to {self.receiver.user.username}"

    def accept(self):
        receiver_friend_list = FriendList.objects.get(user_profile=self.receiver)
        if receiver_friend_list:
            receiver_friend_list.add_friend(self.sender)
            sender_friend_list = FriendList.objects.get(user_profile=self.sender)
            if sender_friend_list:
                sender_friend_list.add_friend(self.receiver)
                self.status = 'Accepted'
                self.save()

    def decline(self):
        self.status = 'Declined'
        self.save()

    def cancel(self):
        self.status = 'Declined'
        self.save()