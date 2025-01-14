from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.crypto import get_random_string
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

from tournaments.models import Tournament, TournamentPlayer, TournamentGame


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
