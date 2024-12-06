from django.test import TestCase
from django.contrib.auth.models import User
from .models import FriendList, FriendRequest
from django.core.exceptions import ValidationError

class FriendRequestModelTest(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username='user1', password='password123')
        self.user2 = User.objects.create_user(username='user2', password='password123')
        self.friend_request = FriendRequest.objects.create(sender=self.user1, receiver=self.user2)

    def test_accept_request(self):
        self.friend_request.accept()
        self.assertEqual(self.friend_request.status, 'Accepted')

        friend_list1 = FriendList.objects.get(user=self.user1)
        friend_list2 = FriendList.objects.get(user=self.user2)
        self.assertIn(self.user2, friend_list1.friends.all())
        self.assertIn(self.user1, friend_list2.friends.all())

    def test_decline_request(self):
        self.friend_request.decline()
        self.assertEqual(self.friend_request.status, 'Declined')

        friend_list1 = FriendList.objects.get(user=self.user1)
        friend_list2 = FriendList.objects.get(user=self.user2)

        # Ensure neither user is in the other's friend list
        self.assertNotIn(self.user2, friend_list1.friends.all())
        self.assertNotIn(self.user1, friend_list2.friends.all())

        # Ensure the friend request is not in the pending friend requests
        pending_requests = FriendRequest.objects.filter(sender=self.user1, receiver=self.user2, status='Pending')
        self.assertEqual(pending_requests.count(), 0)

    def test_cancel_request(self):
        self.friend_request.cancel()
        self.assertEqual(self.friend_request.status, 'Declined')

    def test_cannot_send_self_friend_request(self):
        with self.assertRaises(ValidationError) as context:
            FriendRequest.objects.create(sender=self.user1, receiver=self.user1)
        self.assertIn(
            "Users cannot send friend requests to themselves.",
            str(context.exception)
        )
