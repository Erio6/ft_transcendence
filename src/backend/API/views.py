from django.shortcuts import render
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from game.models import Game
from dashboard.models import GameHistory
from .serializers import GameSerializer, GameHistorySerializer


# Create your views here.

class ScoreView(APIView):
    def post(self, request):
        serializer = GameSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




class GameHistoryView(APIView):
    def get(self, *args, **kwargs):
        game = GameHistory.objects.all().order_by('-id')
        serializer = GameHistorySerializer(game, many=True)
        return Response(serializer.data)

