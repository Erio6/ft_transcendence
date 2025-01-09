from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.shortcuts import redirect
from dashboard.models import GameHistory
from user.models import UserProfile

def home(request):
    game_histories = GameHistory.objects.order_by('-date_played')[:10]

    # Build a list of game details
    history_data = []
    for history in game_histories:
        game = history.game_object  # Dynamically fetch the related game object
        if game:
            history_data.append({
                'player_one': game.player_one,
                'player_two': game.player_two,
                'player_one_score': game.player_one_score,
                'player_two_score': game.player_two_score,
                'winner': game.winner,
                'date_played': history.date_played,
            })
    profile = None
    if request.user.is_authenticated:
        profile = UserProfile.objects.get(user=request.user)

    context = {
        'user': request.user,
        'game_histories': history_data,
        'profile': profile,
    }
    return render(request, 'djangoProject/home.html', context)