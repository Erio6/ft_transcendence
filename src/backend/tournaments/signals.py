from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.db import transaction
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db.models import Max
from django.utils import timezone
from game.models import Game
from tournaments.models import TournamentGame, Tournament, TournamentPlayer
from user.models import UserProfile

@receiver(post_save, sender=Game)
def handle_game_completion(sender, instance, **kwargs):
    if instance.is_completed and instance.type_of_game == 'tournament' and not instance.winner_score == 0 and not kwargs.get('created', False):
        try:
            tournament_game = TournamentGame.objects.get(game=instance)
            tournament = tournament_game.tournament
            winner = instance.winner

            with transaction.atomic():
                winner_tp = TournamentPlayer.objects.get(tournament=tournament, player=winner)
                tournament_game.winner = winner_tp
                tournament_game.save()

                max_round = TournamentGame.objects.filter(
                    tournament=tournament
                ).aggregate(Max('round_number'))['round_number__max']

                final_games = TournamentGame.objects.filter(
                    tournament=tournament,
                    round_number=max_round,
                )

                if all(games.winner for games in final_games):
                    tournament.status = 'completed'
                    tournament.end_date = timezone.now()
                    tournament.save()


                if tournament_game.parent and tournament.status != 'completed':
                    parent_game = tournament_game.parent
                    if parent_game.player_one is None:
                        parent_game.player_one = winner_tp
                    elif parent_game.player_two is None and parent_game.player_one != winner_tp:
                        parent_game.player_two = winner_tp
                    parent_game.save()

                    if parent_game.player_one and parent_game.player_two and not parent_game.game:
                        game_instance = Game.objects.create(
                            player_one=parent_game.player_one.player,
                            player_two=parent_game.player_two.player,
                            type_of_game='tournament',
                        )
                        parent_game.game = game_instance
                        parent_game.save()

                # max_round = TournamentGame.objects.filter(
                #     tournament=tournament
                # ).aggregate(Max('round_number'))['round_number__max']
                #
                # final_games = TournamentGame.objects.filter(
                #     tournament=tournament,
                #     round_number=max_round,
                # )
                #
                # if all(games.winner for games in final_games):
                #     tournament.status = 'completed'
                #     tournament.end_date = timezone.now()
                #     tournament.save()

                channel_layer = get_channel_layer()
                async_to_sync(channel_layer.group_send)(
                    f"tournament_{tournament.id}",
                    {
                        'type': 'tournament_data_update',
                        'action': 'game_completed',
                        'game_id': tournament_game.id,
                        'winner': winner.id,
                        'is_final': tournament.status == 'completed'
                    }
                )

        except Exception as e:
            print(f"Error handling game completion: {str(e)}")