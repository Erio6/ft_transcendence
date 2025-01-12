from django.shortcuts import render

# Create your views here.

def tournaments_home(request):
    return render(request, 'tournaments/tournament_home.html')

#def create_tournament(request):

#def join_tournament(request):