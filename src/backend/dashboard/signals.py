from django.db.models.signals import post_save
from django.db.models import F
from django.dispatch import receiver
from django.contrib.contenttypes.models import ContentType
from game.models import Game
from tournaments.models import TournamentGame


def update_ranks():
    from .models import Leaderboard
    leaderboard_entries = Leaderboard.objects.all().order_by('-elo')

    # Assign ranks based on total_points
    for rank, leaderboard in enumerate(leaderboard_entries, 1):  # Rank starts from 1
        leaderboard.rank = rank
        leaderboard.save()


@receiver(post_save, sender=Game)
def log_multiplayer_game(sender, instance, created, **kwargs):
    # Trigger only when the game is marked as completed
    print("Before")
    if instance.is_completed and not instance.winner_score == 0 and instance.type_of_game == "multiplayer":
        print("after")
        from .models import GameHistory
        from .models import Leaderboard
        # Log the game in history
        GameHistory.objects.create(
            game_type=ContentType.objects.get_for_model(Game),
            game_id=instance.id
        )

        leaderboard_one, created = Leaderboard.objects.get_or_create(player=instance.player_one)
        leaderboard_two, created = Leaderboard.objects.get_or_create(player=instance.player_two)

        leaderboard_one.update_player_stats(
            opponent_leaderboard=leaderboard_two,
            is_winner=(instance.winner == instance.player_one),
        )

        leaderboard_two.update_player_stats(
            opponent_leaderboard=leaderboard_one ,
            is_winner=(instance.winner == instance.player_two),
        )

        leaderboard_one.update_elo(
            opponent_leaderboard=leaderboard_two,
            is_winner=(instance.winner == instance.player_one),
        )

        leaderboard_two.update_elo(
            opponent_leaderboard=leaderboard_one,
            is_winner=(instance.winner == instance.player_two),
        )
        update_ranks()

# @receiver(post_save, sender=SoloGame)
# def log_solo_game(sender, instance, created, **kwargs):
#     # Trigger only when the game is marked as completed
#     if instance.is_completed:
#         # Log the game in history
#         GameHistory.objects.create(
#             game_type=ContentType.objects.get_for_model(SoloGame),
#             game_id=instance.id
#         )
#         # Update the leaderboard
#         Leaderboard.update_player_stats(instance.player_solo, instance.player_solo_score, win=(instance.winner == instance.player_solo))
