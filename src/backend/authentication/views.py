from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django_otp import devices_for_user
from user.models import UserProfile

def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request,form.save())
            user.userprofile.is_online = True
            user.userprofile.save()
            return redirect("/")
    else:
        form = UserCreationForm()
    return render(request, "authentication/register.html", {"form": form})

def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            #if devices_for_user(user, confirmed=True):
            #    return redirect('two_factor:login')
            login(request,user)
            user.userprofile.is_online = True
            user.userprofile.save()
            return redirect("/")
    else:
        form = AuthenticationForm()
    return render(request, "authentication/login.html", {"form": form})

def logout_view(request):
    if request.user.is_authenticated:
        request.user.userprofile.is_online = False
        request.user.userprofile.save()
    logout(request)
    return redirect("/")
