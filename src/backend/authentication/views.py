from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django_otp import devices_for_user
"""from .forms import UserRegistrationForm"""
from django.contrib.auth.views import LoginView
from user.models import User
from user.models import UserProfile
from django.contrib.sites.shortcuts import get_current_site
from django.dispatch import receiver
from django.contrib.auth.signals import user_logged_in

def login_view(request):
	return redirect('two_factor:login')


def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)

            # Simulate the login signal
            user_logged_in.send(sender=user.__class__, request=request, user=user)

            return redirect("two_factor:setup")
    else:
        form = UserCreationForm()
    return render(request, "authentication/register.html", {"form": form})

from django.shortcuts import redirect
from django.contrib.auth import logout
from django.http import JsonResponse

def logout_view(request):
    response = redirect("/")  # Redirect to home or login page
    logout(request)

    # Clear the JWT cookies
    response.delete_cookie("access_token")
    response.delete_cookie("refresh_token")
    return response

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def protected_view(request):
    return Response({"message": f"Hello, {request.user.username}! You are authenticated."})