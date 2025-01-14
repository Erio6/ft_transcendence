from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.crypto import get_random_string
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from django.db import transaction
from math import ceil, log2

from tournaments.models import Tournament, TournamentPlayer, TournamentGame

import random


# Create your views here.

def tournaments_home(request):
    return render(request, 'tournaments/tournament_home.html')


@login_required
def create_tournament(request):
    if request.method == 'POST':
        name = request.POST['name']
        code = get_random_string(4)

        tournament = Tournament.objects.create(
            name=name,
            created_by=request.user.userprofile,
            tournament_code_join=code
        )
        TournamentPlayer.objects.create(tournament=tournament, player=request.user.userprofile)
        print("*************Tournament ID : ")
        print(tournament.id)
        return redirect('tournaments:waiting_room', tournament_id=tournament.id)

    return render(request, 'tournaments/create_tournament.html')

@login_required
def join_tournament(request):
    if request.method == 'POST':
        code = request.POST['code']

        tournament = Tournament.objects.filter(tournament_code_join=code, status='waiting').first()
        if tournament:
            if TournamentPlayer.objects.filter(tournament=tournament, player=request.user.userprofile).exists():
                return redirect(request,'tournaments:waiting_room', tournament_id=tournament.id)
            TournamentPlayer.objects.create(tournament=tournament, player=request.user.userprofile)
            return redirect('tournaments:waiting_room', tournament_id=tournament.id)
        else:
            return render(request, 'tournaments/join_tournament.html',
                          {'error': 'Invalid tournament code or tournament has already started.'})

    return render(request, 'tournaments/join_tournament.html')

@login_required
def tournament_waiting_room(request, tournament_id):
    tournament = get_object_or_404(Tournament, id=tournament_id)
    print("*************Tournament ID 2: ")
    print(tournament.id)
    players = TournamentPlayer.objects.filter(tournament=tournament)
    return render(request, 'tournaments/tournament_waiting_room.html', {
        'tournament': tournament,
        'players': players,
        'current_user': request.user,
    })

@login_required
def cancel_tournament(request, tournament_id):
    tournament = get_object_or_404(Tournament, id=tournament_id, created_by=request.user.userprofile)

    group_name = f'tournament_{tournament.id}'
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        group_name,
        {
            'type': 'handle_tournament_cancel',
        }
    )

    tournament.delete()
    return redirect('tournaments:tournaments')

@login_required
def leave_tournament(request, tournament_id):
    tournament = get_object_or_404(Tournament, id=tournament_id)
    player = TournamentPlayer.objects.filter(tournament=tournament, player=request.user.userprofile).first()

    # Make sure that the creator cannot leave the tournament, he can only cancel it
    if player:
        if tournament.created_by == request.user.userprofile:
            return redirect('tournaments:waiting_room', tournament_id=tournament.id)

        group_name = f'tournament_{tournament.id}'
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            group_name,
            {
                'type': 'handle_player_leave',
            }
        )

        player.delete()

    return redirect('tournaments:tournaments')

@login_required
def start_tournament(request, tournament_id):
    tournament = get_object_or_404(Tournament, id=tournament_id, created_by=request.user.userprofile)

    if tournament.created_by != request.user.userprofile:
        return redirect('tournaments:waiting_room', tournament_id=tournament.id)

    players = list(TournamentPlayer.objects.filter(tournament=tournament))
    if len(players) < 4:
        return redirect('tournaments:waiting_room', tournament_id=tournament.id)

    total_rounds = ceil(log2(len(players)))

    with transaction.atomic():
        tournament.status = 'ongoing'
        tournament.save()

        random.shuffle(players)

        num_byes = (2 ** total_rounds) - len(players)
        bye_players = [None] * num_byes
        player_slots = players + bye_players

        round_number = 1
        games = []
        for i in range(0, len(player_slots), 2):
            player_one = player_slots[i].player if i < len(players) else None
            player_two = player_slots[i + 1].player if i + 1 < len(players) else None
            games.append(
                TournamentGame(
                    tournament=tournament,
                    round_number=round_number,
                    player_one=player_one,
                    player_two=player_two,
                )
            )

        TournamentGame.objects.bulk_create(games)

    return redirect('tournaments:tournament_tree', tournament_id=tournament.id)

@login_required
def tournament_tree_view(request, tournament_id):
    tournament = get_object_or_404(Tournament, id=tournament_id)
    games = TournamentGame.objects.filter(tournament=tournament).order_by('round_number')
    current_user = request.user.userprofile

    nodes = []
    for game in games:
        match_node = {
            "key": f"match-{game.id}",
            "text": f"Match {game.round_number}-{game.id}",
            "round": game.round_number,
            "player_one": game.player_one.display_name if game.player_one else None,
            "player_two": game.player_two.display_name if game.player_two else None,
            "winner": game.winner.display_name if game.winner else None,
        }
        match_node = {k: (v if v is not None else None) for k, v in match_node.items()}
        nodes.append(match_node)

        if game.player_one:
            nodes.append(
                {"key": f"player-{game.player_one.id}",
                 "text": game.player_one.display_name,
                 "isPlayer": True,
                 "color": "red" if current_user == game.player_one else "lightblue",})

        if game.player_two:
            nodes.append(
                {"key": f"player-{game.player_two.id}",
                 "text": game.player_two.display_name,
                 "isPlayer": True,
                 "color": "red" if current_user == game.player_two else "lightblue",})

    links = []
    for game in games:
        if game.player_one:
            links.append(
                {"from": f"player-{game.player_one.id}",
                 "to": f"match-{game.id}"})
        if game.player_two:
            links.append(
                {"from": f"player-{game.player_two.id}",
                 "to": f"match-{game.id}"})

        if game.winner:
            next_match = TournamentGame.objects.filter(tournament=tournament, round_number=game.round_number + 1).first()
            if next_match:
                links.append(
                    {"from": f"match-{game.id}",
                     "to": f"match-{next_match.id}"})


    # games_by_round = {}
    # for game in TournamentGame.objects.filter(tournament=tournament).order_by('round_number'):
    #     games_by_round.setdefault(game.round_number, []).append(game)

    return render(request, 'tournaments/tournament_tree.html', {
        'tournament': tournament,
        'nodes': nodes,
        'links': links,
    })


