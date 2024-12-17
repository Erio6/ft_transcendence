from django.shortcuts import render
from .models import Leaderboard, GameHistory

# Create your views here.

def leaderboard(request):
    leaderboard = Leaderboard.objects.all().order_by('rank')

    return render(request, 'dashboard/leaderboard.html', {'leaderboard': leaderboard})


# def game_history_view(request):
#     game_histories = GameHistory.objects.order_by('date_played')[:10]
#
#     history_data = []
#     for history in game_histories:
#         game = history.game_object
#         if game:
#             history_data.append({
#                 'player_one': game.player_one,
#                 'player_two': game.player_two,
#                 'player_one_score': game.player_one_score,
#                 'player_two_score': game.player_two_score,
#                 'winner': game.winner,
#                 'date_played': history.date_played,
#             })
#
#     context = {
#         'game_histories': history_data,
#     }
#     return render(request, 'game_history.html', context)