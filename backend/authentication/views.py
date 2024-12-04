from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django_otp import devices_for_user

"""from .forms import UserRegistrationForm"""
from django.contrib.auth.views import LoginView

def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            login(request,form.save())
            return redirect("/")
    else:
        form = UserCreationForm()
    return render(request, "authentication/register.html", {"form": form})

def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            if devices_for_user(user, confirmed=True):
                return redirect('two_factor:profile')
            #login(request,user)
            return redirect("/")
    else:
        form = AuthenticationForm()
    return render(request, "authentication/login.html", {"form": form})

def logout_view(request):
        logout(request)
        return redirect("/")
