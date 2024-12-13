
from django.db import models
from django.core.exceptions import ValidationError
from user.models import UserProfile


class FriendList(models.Model):
    user = models.OneToOneField(UserProfile, on_delete=models.CASCADE, related_name='friend_list')
    friends = models.ManyToManyField(UserProfile, blank=True, related_name='friends')

    def __str__(self):
        return self.user.user.username

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
        friends_list.remove_friend(self.user)

    def is_mutual_friend(self, friend):
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

    def save(self, *args, **kwargs):
        if self.sender == self.receiver:
            raise ValidationError("Users cannot send friend requests to themselves.")
        super().save(*args, **kwargs)

    def accept(self):
        receiver_friend_list = FriendList.objects.get(user=self.receiver)
        if receiver_friend_list:
            receiver_friend_list.add_friend(self.sender)
            sender_friend_list = FriendList.objects.get(user=self.sender)
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



# Create your models here.
