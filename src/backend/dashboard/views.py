from django.shortcuts import render
from django.db.models import Q
from .models import Leaderboard, GameHistory, SoloGame , Game
from user.models import UserProfile
from django.contrib.contenttypes.models import ContentType

# Create your views here.

def leaderboard(request):
    leaderboard = Leaderboard.objects.all().order_by('rank')
    profile = None
    if request.user.is_authenticated:
        profile = UserProfile.objects.get(user=request.user)

    context = {
        'profile': profile,
        'leaderboard': leaderboard,
    }

    return render(request, 'dashboard/leaderboard.html', context)

def dashboard(request):
    profile = None
    leaderboard = Leaderboard.objects.all().order_by('rank')
    user_entry = leaderboard.filter(player__user=request.user).first()
    leaderboard_without_user = leaderboard.exclude(player__user=request.user)

    if user_entry:
        leaderboard = [user_entry] + list(leaderboard_without_user)
    else:
        leaderboard = leaderboard_without_user

    game_histories = []
    if request.user.is_authenticated:
        profile = UserProfile.objects.get(user=request.user)
        user_entry = Leaderboard.objects.filter(player=profile).first()
        game_type = ContentType.objects.get_for_model(Game)
        game_histories = GameHistory.objects.filter(
            game_type=game_type,
            game_id__in=Game.objects.filter(
                Q(player_one=profile) | Q(player_two=profile)
            ).values_list('id', flat=True)
        ).order_by('-date_played')[:4]

        history_data = []
        for history in game_histories:
            game = history.game_object
            if game:
                history_data.append({
                    'player_one': game.player_one,
                    'player_two': game.player_two,
                    'player_one_score': game.player_one_score,
                    'player_two_score': game.player_two_score,
                    'winner': game.winner,
                    'date_played': history.date_played,
                })

        context = {
            'profile': profile,
            'leaderboard': leaderboard,
            'user_entry': user_entry,
            'game_histories': history_data,
        }

    return render(request, 'dashboard/dashboard.html', context)


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