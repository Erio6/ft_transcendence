from django.shortcuts import render, redirect, reverse
from django.contrib import messages
from .models import Match
from user.models import UserProfile
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

# Create your views here.

@api_view(["GET", "POST"])
@permission_classes([IsAuthenticated])
def waiting_view(request):
    if not request.user.is_authenticated:
        return redirect("authentication:login")

    user_profile = UserProfile.objects.get(user=request.user)

    match = Match.objects.filter(player_two__isnull=True, status='waiting').first()
    if match and match.player_one != user_profile:
        match.player_two = user_profile
        print(match.player_one, match.player_two, match.id)
        match.status = 'matched'
        match.save()
    elif not match:
        match = Match.objects.create(player_one=user_profile, status='waiting')
        print("****IM HERE!!****")
    else:
        print(match.player_one, user_profile)
        messages.error(request, "You are already looking for a match")
        return redirect("game:play")
    home = 'game:play'
    print(match.id)
    context = {
        "match_id": match.id,
        "profile": user_profile,
        "home": home
    }
    return render(request, 'matchMaking/waiting.html', context)
