from django.shortcuts import render
from rest_framework import status, permissions
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from web3 import Web3
from game.models import Game
from dashboard.models import GameHistory
from .serializers import GameSerializer, GameHistorySerializer, BlockchainStatusSerializer
from django.conf import settings
from user.models import UserProfile


# Create your views here.

@api_view(['POST'])
def game_update(request):
    game_id = request.data.get('game_id')

    try:
        game = Game.objects.get(id=game_id)
    except Game.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = GameSerializer(game, data=request.data, partial=True)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GameHistoryView(APIView):
    def get(self, *args, **kwargs):
        game = GameHistory.objects.all().order_by('-id')
        serializer = GameHistorySerializer(game, many=True)
        return Response(serializer.data)

class IsParticipant(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        try:
            user_profile = request.user.userprofile
        except UserProfile.DoesNotExist:
            return False

        is_participant = user_profile == obj.winner or user_profile == obj.looser
        return is_participant

class CheckTransactionStatus(APIView):
    permission_classes = [permissions.IsAuthenticated, IsParticipant]

    def get_object(self, game_id):
        game = get_object_or_404(Game, pk=game_id)
        self.check_object_permissions(self.request, game)
        return game

    def get(self, request, game_id):
        game = self.get_object(game_id)

        if not game.tx_hash:
            return Response({'status': 'no_transaction'}, status=status.HTTP_200_OK)

        try:
            web3 = Web3(Web3.HTTPProvider(settings.WEB3_PROVIDER_URI))
            receipt = web3.eth.get_transaction_receipt(game.tx_hash)
        except Exception as e:
            return Response({'status': 'error', 'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        if receipt and receipt.status == 1:
            tx_url = f"https://sepolia.etherscan.io/tx/0x{game.tx_hash}"
            return Response({'status': 'completed', 'tx_url': tx_url, 'tx_hash': game.tx_hash},
                            status=status.HTTP_200_OK)
        else:
            return Response({'status': 'pending'}, status=status.HTTP_200_OK)

