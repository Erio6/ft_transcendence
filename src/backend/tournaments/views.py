from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.utils.crypto import get_random_string

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

        return redirect('tournaments:waiting_room', tournament_id=tournament.id)

    return render(request, 'tournaments/create_tournament.html')

@login_required
def join_tournament(request):
    if request.method == 'POST':
        code = request.POST['code']

        tournament = Tournament.objects.filter(tournament_code_join=code, status='waiting').first()
        if tournament:
            TournamentPlayer.objects.create(tournament=tournament, player=request.user.userprofile)
            return redirect('tournaments:waiting_room', tournament_id=tournament.id)
        else:
            return render(request, 'tournaments/join_tournament.html',
                          {'error': 'Invalid tournament code or tournament has already started.'})

    return render(request, 'tournaments/join_tournament.html')

