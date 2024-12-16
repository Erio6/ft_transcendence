from rest_framework import serializers
from dashboard.models import GameHistory
from game.models import Game
from user.models import UserProfile

class GameSerializer(serializers.ModelSerializer):
    winner = serializers.PrimaryKeyRelatedField(queryset=UserProfile.objects.all())
    looser = serializers.PrimaryKeyRelatedField(queryset=UserProfile.objects.all())

    class Meta:
        model = Game
        fields = ['id', 'player_one_score', 'player_two_score', 'winner', 'looser', 'is_completed']

    def update(self, instance, validated_data):
        # winner_id = validated_data.get('winner', None)
        # looser_id = validated_data.get('looser', None)
        #
        # if winner_id:
        #     winner = UserProfile.objects.get(id=winner_id)
        #     instance.winner = winner
        #
        # if looser_id:
        #     looser = UserProfile.objects.get(id=looser_id)
        #     instance.looser = looser
        #
        # instance.player_one_score = validated_data.get('player_one_score', instance.player_one_score)
        # instance.player_two_score = validated_data.get('player_two_score', instance.player_two_score)

        instance.winner = validated_data.get('winner', instance.winner)
        instance.looser = validated_data.get('looser', instance.looser)

        instance.player_one_score = validated_data.get('player_one_score', instance.player_one_score)
        instance.player_two_score = validated_data.get('player_two_score', instance.player_two_score)

        if instance.winner == instance.player_one:
            instance.winner_score = instance.player_one_score
            instance.looser_score = instance.player_two_score
        elif instance.winner == instance.player_two:
            instance.winner_score = instance.player_two_score
            instance.looser_score = instance.player_one_score

        instance.is_completed = validated_data.get('is_completed', instance.is_completed)

        instance.save()
        return instance

class GameHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = GameHistory
        fields = '__all__'