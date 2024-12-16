from django.shortcuts import render
from .models import Leaderboard

# Create your views here.

def leaderboard(request):
    leaderboard = Leaderboard.objects.all().order_by('rank')

    return render(request, 'dashboard/leaderboard.html', {'leaderboard': leaderboard})
