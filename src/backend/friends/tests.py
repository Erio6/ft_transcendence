from django.test import TestCase
from django.contrib.auth.models import User
from .models import FriendList, FriendRequest
from django.core.exceptions import ValidationError
from user.models import UserProfile

class FriendRequestModelTest(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username='user1', password='password123')
        self.user2 = User.objects.create_user(username='user2', password='password123')
        self.user1_profile = UserProfile.objects.get(user=self.user1)
        self.user2_profile = UserProfile.objects.get(user=self.user2)
        self.friend_request = FriendRequest.objects.create(sender=self.user1_profile, receiver=self.user2_profile)

    def test_accept_request(self):
        self.friend_request.accept()
        self.assertEqual(self.friend_request.status, 'Accepted')

        friend_list1 = FriendList.objects.get(user=self.user1_profile)
        friend_list2 = FriendList.objects.get(user=self.user2_profile)
        self.assertIn(self.user2_profile, friend_list1.friends.all())
        self.assertIn(self.user1_profile, friend_list2.friends.all())

    def test_decline_request(self):
        self.friend_request.decline()
        self.assertEqual(self.friend_request.status, 'Declined')

        friend_list1 = FriendList.objects.get(user=self.user1_profile)
        friend_list2 = FriendList.objects.get(user=self.user2_profile)

        self.assertNotIn(self.user2_profile, friend_list1.friends.all())
        self.assertNotIn(self.user1_profile, friend_list2.friends.all())

        pending_requests = FriendRequest.objects.filter(sender=self.user1_profile, receiver=self.user2_profile, status='Pending')
        self.assertEqual(pending_requests.count(), 0)

    def test_cancel_request(self):
        self.friend_request.cancel()
        self.assertEqual(self.friend_request.status, 'Declined')

    def test_cannot_send_self_friend_request(self):
        with self.assertRaises(ValidationError) as context:
            FriendRequest.objects.create(sender=self.user1_profile, receiver=self.user1_profile)
        self.assertIn(
            "Users cannot send friend requests to themselves.",
            str(context.exception)
        )
