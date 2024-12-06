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
from two_factor.signals import user_verified

def login_view(request):
	return redirect('two_factor:login')


def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("two_factor:setup")
    else:
        form = UserCreationForm()
    return render(request, "authentication/register.html", {"form": form})

def logout_view(request):
        logout(request)
        return redirect("/")

