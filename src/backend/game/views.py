from contextlib import nullcontext
from xxlimited_35 import error

from django.shortcuts import render, redirect, get_object_or_404

from .forms import ScoreInputForm
from .models import Game
from user.models import UserProfile


def quickPlay(request):
    return render(request, 'game/playmode.html')


def soloGame(request):
    return render(request, 'game/sologame.html')


def multiGame(request):
    return render(request, 'game/multisearch.html')


def game_creation(request):
    if request.method == 'POST':
        player_one_id = request.POST.get('player_one')
        player_two_id = request.POST.get('player_two')

        player_one = UserProfile.objects.get(id=player_one_id)
        player_two = UserProfile.objects.get(id=player_two_id)
        new_game = Game(player_one=player_one, player_two=player_two)
        new_game.save()

        return redirect(f'multi_scores/{new_game.id}')

    users = UserProfile.objects.all()
    return render(request, 'game/multi_game.html', {"users": users})


def multi_scores(request, game_id):
    try:
        game = Game.objects.get(id=game_id)
    except Game.DoesNotExist:
        return redirect(error, 'Game does not exist')
    return render(request, 'game/multiscores.html', {"game": game})


def online_game_creation(request):
    # print(request.user.id, UserProfile.objects.get(id=request.user.id))
    games = Game.objects.filter(is_completed=False).all()
    return render(request, 'game/online.html', {"games": games})


def game_3d(request, game_id):
    if not Game.objects.filter(id=game_id).exists():
        print("Game does not exist")
        return redirect('/')
    print("load threejs.html")
    return render(request, 'game/threejs.html')

# def test_pong_game(request):
#     if request.method == "POST":
#         form = ScoreInputForm(request.POST)
#         if form.is_valid():
#             player_one = form.cleaned_data['player_one']
#             player_two = form.cleaned_data['player_two']
#             player_one_score = form.cleaned_data['player_one_score']
#             player_two_score = form.cleaned_data['player_two_score']
#
#             player_one_profile, _ = UserProfile.objects.get_or_create(user=player_one)
#             player_two_profile, _ = UserProfile.objects.get_or_create(user=player_two)
#
#             if player_one_score > player_two_score:
#                 player_one_profile.wins += 1
#                 player_two_profile.losses += 1
#                 player_one_profile.total_points += player_one_score
#                 player_two_profile.total_points += player_two_score
#                 winner_score = player_one_score
#                 looser_score = player_two_score
#                 winner = player_one_profile
#                 looser = player_two_profile
#                 result_message = f"{player_one.username} wins!"
#             elif player_one_score < player_two_score:
#                 player_two_profile.wins += 1
#                 player_one_profile.losses += 1
#                 player_two_profile.total_points += player_two_score
#                 player_one_profile.total_points += player_one_score
#                 winner_score = player_two_score
#                 looser_score = player_one_score
#                 winner = player_two_profile
#                 looser = player_one_profile
#                 result_message = f"{player_two.username} wins!"
#             else:
#                 player_one_profile.draws += 1
#                 player_two_profile.draws += 1
#                 player_two_profile.total_points += player_two_score
#                 player_one_profile.total_points += player_one_score
#                 result_message_draw = "It's a draw!"
#
#                 return render(request, "game/multi_game_result.html", {
#                     "form": form,
#                     "result_message_draw": result_message_draw,
#                     "player_one_profile": player_one_profile,
#                     "player_two_profile": player_two_profile,
#                     "player_one_score": player_one_score,
#                     "player_two_score": player_two_score,
#                 })
#
#             player_one_profile.save()
#             player_two_profile.save()
#
#             return render(request, "game/multi_game_result.html", {
#                 "form": form,
#                 "result_message": result_message,
#                 "winner": winner,
#                 "looser": looser,
#                 "winner_score": winner_score,
#                 "looser_score": looser_score,
#             })
#     else:
#         form = ScoreInputForm()
#
#     return render(request, "game/multi_game.html", {"form": form})


# plan : faire une page pour creer une game et passer l'id de la game en url.
# Ensuite une page pour rentrer les scores et faire un post pour remplir la db et tester le reste.
