from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.shortcuts import redirect
from dashboard.models import GameHistory
from user.models import UserProfile

def home(request):
    game_histories = GameHistory.objects.order_by('-date_played')[:10]

    # Build a list of game details
    history_data = []
    seen_game_ids = set()
    for history in game_histories:
        if history.game_id in seen_game_ids:
            continue  # Skip duplicate game_id
        seen_game_ids.add(history.game_id)
        game = history.game_object  # Dynamically fetch the related game object
        if game:
            history_data.append({
                'game_id': history.game_id,
                'player_one': game.player_one,
                'player_two': game.player_two,
                'player_one_score': game.player_one_score,
                'player_two_score': game.player_two_score,
                'winner': game.winner,
                'date_played': history.date_played,
                'tx_hash': game.tx_hash,
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

def our_team(request):
    profile = UserProfile.objects.get(user=request.user)
    context = {
        'user': request.user,
        'profile': profile,
    }
    return render(request, 'djangoProject/our_team.html',context)