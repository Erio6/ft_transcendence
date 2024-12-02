from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from .forms import UserUpdateForm, ProfileUpdateForm
from django.contrib.auth.models import User
from .models import UserProfile, FriendList , FriendRequest
from django.contrib import messages

def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            login(request,form.save())
            return redirect("game:welcome")
    else:
        form = UserCreationForm()
    return render(request, "authentication/register.html", {"form": form})

def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            if "next" in request.POST:
                return redirect(request.POST.get("next"))
            else:
                return redirect("game:welcome")
    else:
        form = AuthenticationForm()
    return render(request, "authentication/login.html", {"form": form})

def logout_view(request):
        logout(request)
        return redirect("game:welcome")

@login_required(login_url='authentication:login')
def profile_view(request,username):
        user = get_object_or_404(User, username=username)
        profile = get_object_or_404(UserProfile, user=user)
        context = {
            'profile': profile,
        }
        return render(request, 'authentication/profile.html', context)

def edit_profile_view(request,username):
    if request.user.username != username:
        messages.error(request, "You do not have the right to modify this profile.")
        return redirect('authentication:user_profile', username=username)

    profile = get_object_or_404(UserProfile,user=request.user)

    if request.method == "POST":
        form = ProfileUpdateForm(request.POST,
                                    request.FILES,
                                    instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('authentication:user_profile', username=username)
    else:
        form = ProfileUpdateForm(instance=profile)

    context = {
        'form': form,
        'profile': profile
    }
    return render(request, 'authentication/edit_profile.html',context)

# FRIENDS VIEWS

