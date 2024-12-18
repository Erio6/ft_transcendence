from django.shortcuts import render
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from game.models import Game
from dashboard.models import GameHistory
from .serializers import GameSerializer, GameHistorySerializer


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

