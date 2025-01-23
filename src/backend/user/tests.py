from django.test import TestCase
from user.models import UserProfile
from django.contrib.auth.models import User

class UserProfileTestCase(TestCase):
    def setUp(self):
        user1 = User.objects.create(username="player1")
        user2 = User.objects.create(username="player2")


        self.player1_profile = user1.userprofile
        self.player2_profile = user2.userprofile

        self.player1_profile.elo_rating = 1500
        self.player2_profile.elo_rating = 1600

        self.player1_profile.save()
        self.player2_profile.save()

    def test_update_elo(self):
        self.assertEqual(self.player1_profile.elo_rating, 1500)
        self.assertEqual(self.player2_profile.elo_rating, 1600)


        self.player1_profile.update_elo(self.player2_profile, is_winner=True)
        self.assertNotEqual(self.player1_profile.elo_rating, 1500)
        self.assertNotEqual(self.player2_profile.elo_rating, 1600)