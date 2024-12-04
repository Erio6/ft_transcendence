from django.shortcuts import render, redirect
from .forms import ScoreInputForm
from .models import Game

def welcome(request):
    return render(request, 'game/welcome.html', context={"name": "Player"})

def quickPlay(request):
    return render(request, 'game/playmode.html')

def soloGame(request):
    return render(request, 'game/sologame.html')

def multiGame(request):
    return render(request, 'game/multisearch.html')

def test_pong_game(request):
    if request.method == "POST":
        form = ScoreInputForm(request.POST)
        if form.is_valid():
            player_one = form.cleaned_data['player_one']
            player_two = form.cleaned_data['player_two']
            player_one_score = form.cleaned_data['player_one_score']
            player_two_score = form.cleaned_data['player_two_score']

            if player_one_score > player_two_score:
                winner = player_one
                looser = player_two
                winner_score = player_one_score
                looser_score = player_two_score
            else:
                winner = player_two
                looser = player_one
                winner_score = player_two_score
                looser_score = player_one_score

            Game.objects.create(
                player_one=player_one,
                player_two=player_two,
                player_one_score=player_one_score,
                player_two_score=player_two_score,
                winner=winner,
                looser=looser,
                winner_score=winner_score,
                looser_score=looser_score,
            )

            return render(request, "game/multi_game_result.html", {
                "winner": winner,
                "winner_score": winner_score,
                "looser": looser,
                "looser_score": looser_score,
            })
    else:
        form = ScoreInputForm()

    return render(request, "game/multi_game.html", {"form": form})