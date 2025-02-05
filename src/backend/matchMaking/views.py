from django.shortcuts import render, redirect, reverse
from django.contrib import messages
from .models import Match
from user.models import UserProfile

# Create your views here.


# - faire une class match avec les infos des deux players dedans, si un des deux player quitte la page ca me supprime le match. La Game est cree uniquement dans le jeux.
# - Faire une websocket avec les deux player et rediriger les deux joueurs dans l'url de la game. D'autres check seront fait dans le serveur du jeux pour s'assurer que les joueurs ont le droit d'etre la.
# - Une fois que les deux utilisateurs sont connectes au websocket, je cree un objet game et ensuite je les envois dans la view 3d-game (dans le three.js)

def waiting_view(request):
    if not request.user.is_authenticated:
        return redirect("authentication:login")

    user_profile = UserProfile.objects.get(user=request.user)

    match = Match.objects.filter(player_two__isnull=True, status='waiting').first()
    if match and match.player_one != user_profile:
        match.player_two = user_profile
        match.status = 'matched'
        match.save()
    elif not match:
        match = Match.objects.create(player_one=user_profile, status='waiting')
    else:
        print(match.player_one, user_profile)
        messages.error(request, "You are already looking for a match")
        return redirect("game:play")
    home = 'game:play'
    context = {
        "match_id": match.id,
        "profile": user_profile,
        "home": home
    }
    return render(request, 'matchMaking/waiting.html', context)



