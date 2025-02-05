from contextlib import nullcontext
from xxlimited_35 import error

from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
from django.http import HttpResponseForbidden
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

from .forms import GameCreationForm
from .models import Game
from user.models import UserProfile
from asgiref.sync import sync_to_async


def quickPlay(request):
    profile = None
    if request.user.is_authenticated:
        profile = UserProfile.objects.get(user=request.user)
    return render(request, 'game/playmode.html', {"profile": profile})


# @api_view(["GET", "POST"])
# @permission_classes([IsAuthenticated])
@login_required
def soloGame(request):
    profile = UserProfile.objects.get(user=request.user)
    if request.method == 'POST':
        print(request.POST)
        form = GameCreationForm(request.POST)
        if form.is_valid():
            print("valid")
            # player_side = form.cleaned_data['player_side']
            game_type = form.cleaned_data['game_type']

            try:
                player_profile = request.user.userprofile
            except UserProfile.DoesNotExist:
                return redirect('user:edit_user_profile', username=request.user.username)

            game = Game.objects.create(player_one=player_profile, is_completed=False, type_of_game=game_type)

            return redirect(reverse('game:real_game', kwargs={'game_id': game.id}))
        else:
            print(form.errors)
    else:
        form = GameCreationForm()
    return render(request, 'game/sologame.html', {'form': form, 'profile': profile})



# @api_view(["GET"])
# @permission_classes([IsAuthenticated])
@login_required
def online_game_creation(request):
    # print(request.user.id, UserProfile.objects.get(id=request.user.id))
    profile = None
    if request.user.is_authenticated:
        profile = UserProfile.objects.get(user=request.user)
    games = Game.objects.filter(is_completed=False).all()
    return render(request, 'game/online.html', {"games": games, "profile": profile})


# @api_view(["GET"])
# @permission_classes([IsAuthenticated])
@login_required
def game_3d(request, game_id):
    if not request.user.is_authenticated:
        return redirect("authentication:login")

    profile = UserProfile.objects.get(user=request.user)
    if not Game.objects.filter(id=game_id).exists():
        print("Game does not exist", game_id)
        return redirect('/')
    return render(request, 'game/threejs.html', {"profile": profile})


# @api_view(["GET"])
# @permission_classes([IsAuthenticated])
@login_required
def game_error(request):
    return render(request, 'game/error.html', {})


# @api_view(["GET", "POST"])
# @permission_classes([IsAuthenticated])
@login_required
def end_game(request, game_id):
    game = get_object_or_404(Game, id=game_id)
    winner_user = game.winner.user
    looser_user = game.looser.user
    current_user_id = request.user.id
    profile = UserProfile.objects.get(user=request.user)

    # if current_user_id != winner_user.id and current_user_id != looser_user.id:
    #     content = render_to_string('game/unauthorized.html')
    #     return HttpResponseForbidden(content)

    context = {
        'game': game,
        'winner': game.winner,
        'looser': game.looser,
        'winner_score': game.winner_score,
        'looser_score': game.looser_score,
        'tx_hash': game.tx_hash,
        'profile': profile,
    }

    # Render the template asynchronously
    return render(request, 'game/end_game.html', context)


