# tests.py
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from django.contrib.auth.models import User
from unittest.mock import patch
from game.models import Game
from rest_framework_simplejwt.tokens import AccessToken

class CheckTransactionStatusTests(APITestCase):
    def setUp(self):

        self.client = APIClient()
        self.winner_user = User.objects.create_user(username='winner', password='password123')
        self.loser_user = User.objects.create_user(username='loser', password='password123')
        self.other_user = User.objects.create_user(username='other', password='password123')
        self.winner = self.winner_user.userprofile
        self.looser = self.loser_user.userprofile
        self.other_user_profile = self.other_user.userprofile

        self.game = Game.objects.create(
            player_one=self.winner,
            player_two=self.looser,
            winner=self.winner,
            looser=self.looser,
            player_one_score=10,
            player_two_score=5,
            winner_score=10,
            looser_score=5,
            tx_hash='0xabc123',  # Example transaction hash
            type_of_game='multiplayer'
        )

        self.url = reverse('API:check_transaction_status', args=[self.game.id])

    def generate_jwt(self, user):
            token = AccessToken.for_user(user)
            return str(token)


    @patch('API.views.Web3')  # Adjust the path based on your project structure
    def test_winner_can_access_api(self, mock_web3):
        # Mock the transaction receipt to simulate a completed transaction
        mock_receipt = mock_web3.return_value.eth.get_transaction_receipt.return_value
        mock_receipt.status = 1  # Transaction successful
        mock_receipt.blockNumber = 123456
        mock_receipt.transactionHash = '0xabc123'

        token = self.generate_jwt(self.winner_user)
        self.client.cookies['access_token'] = token

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], 'completed')
        self.assertIn('tx_url', response.data)
        self.assertEqual(response.data['tx_hash'], self.game.tx_hash)

    @patch('API.views.Web3')  # Adjust the path based on your project structure
    def test_loser_can_access_api(self, mock_web3):
        mock_receipt = mock_web3.return_value.eth.get_transaction_receipt.return_value
        mock_receipt.status = 1  # Transaction successful
        mock_receipt.blockNumber = 123456
        mock_receipt.transactionHash = '0xabc123'

        token = self.generate_jwt(self.loser_user)
        self.client.cookies['access_token'] = token

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], 'completed')
        self.assertIn('tx_url', response.data)
        self.assertEqual(response.data['tx_hash'], self.game.tx_hash)

    @patch('API.views.Web3')  # Ajustez le chemin si nécessaire
    def test_api_fetches_correct_data_from_blockchain(self, mock_web3):
        mock_receipt = mock_web3.return_value.eth.get_transaction_receipt.return_value
        mock_receipt.status = 1  # Transaction réussie
        mock_receipt.blockNumber = 654321
        mock_receipt.transactionHash = '0xdef456'

        token = self.generate_jwt(self.winner_user)
        self.client.cookies['access_token'] = token

        response = self.client.get(self.url)

        print(f"[Test] Response status code: {response.status_code}")
        print(f"[Test] Response data: {response.data}")


        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], 'completed')
        self.assertIn('tx_url', response.data)
        self.assertEqual(response.data['tx_hash'], self.game.tx_hash)
        expected_tx_url = f"https://sepolia.etherscan.io/tx/0x{self.game.tx_hash}"
        self.assertEqual(response.data['tx_url'], expected_tx_url)

    def test_other_user_cannot_access_api(self):

        token = self.generate_jwt(self.other_user)
        self.client.cookies['access_token'] = token

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @patch('API.views.Web3')  # Adjust the path based on your project structure
    def test_no_transaction(self, mock_web3):
        self.game.tx_hash = None
        self.game.save()

        token = self.generate_jwt(self.winner_user)
        self.client.cookies['access_token'] = token

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], 'no_transaction')

    @patch('API.views.Web3')  # Adjust the path based on your project structure
    def test_transaction_pending(self, mock_web3):
        mock_receipt = mock_web3.return_value.eth.get_transaction_receipt.return_value
        mock_receipt.status = 0  # Transaction pending

        token = self.generate_jwt(self.loser_user)
        self.client.cookies['access_token'] = token

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], 'pending')

    @patch('API.views.Web3')  # Adjust the path based on your project structure
    def test_transaction_error(self, mock_web3):
        mock_web3.return_value.eth.get_transaction_receipt.side_effect = Exception('Blockchain error')

        token = self.generate_jwt(self.winner_user)
        self.client.cookies['access_token'] = token

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)
        self.assertEqual(response.data['status'], 'error')
        self.assertEqual(response.data['message'], 'Blockchain error')