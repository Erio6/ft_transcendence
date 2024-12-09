from rest_framework import serializers

from dashboard.models import GameHistory
from game.models import Game
from dashboard.models import GameHistory

class GameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Game
        fields = '__all__'

class GameHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = GameHistory
        fields = '__all__'