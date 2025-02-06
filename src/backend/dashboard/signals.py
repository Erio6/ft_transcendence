import asyncio

from asgiref.sync import sync_to_async, async_to_sync
from django.db.models.signals import post_save
from django.db.models import F
from django.dispatch import receiver
from django.contrib.contenttypes.models import ContentType

from blockchain.utils import blockchain_score_storage
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
    if instance.is_completed and not instance.winner_score == 0 and instance.type_of_game == "multiplayer":
        from .models import GameHistory
        from .models import Leaderboard

        if GameHistory.objects.filter(game_id=instance.id).exists():
            return
        # Log the game in history
        GameHistory.objects.create(
            game_type=ContentType.objects.get_for_model(Game),
            game_id=instance.id
        )

        leaderboard_one, created = Leaderboard.objects.get_or_create(player=instance.player_one)
        leaderboard_two, created = Leaderboard.objects.get_or_create(player=instance.player_two)

        leaderboard_one.update_elo(
            opponent_leaderboard=leaderboard_two,
            is_winner=(instance.winner == instance.player_one),
        )

        leaderboard_two.update_elo(
            opponent_leaderboard=leaderboard_one,
            is_winner=(instance.winner == instance.player_two),
        )

#         async_to_sync(blockchain_recording_task)(instance.id)
#
#
# async def blockchain_recording_task(game_id):
#     print("recording game on blockchain")
#     tx_hash = await blockchain_score_storage(game_id)
#     game = await sync_to_async(Game.objects.get)(pk=game_id)
#     if tx_hash:
#         print(f"Game recorded on blockchain with tx_hash: {tx_hash}")
#         game.tx_hash = tx_hash
#         game.is_recorded_on_blockchain = True
#     else:
#         print("Failed to record game on blockchain.")
#
#     await sync_to_async(game.save)(force_update=True)

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
