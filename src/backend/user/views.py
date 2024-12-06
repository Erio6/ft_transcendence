from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import UserUpdateForm, ProfileUpdateForm
from django.contrib.auth.models import User
from .models import UserProfile
from django.contrib import messages
from django.shortcuts import render
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash

@login_required(login_url='authentication:login')
def profile_view(request,username):
        user = get_object_or_404(User, username=username)
        profile = get_object_or_404(UserProfile, user=user)
        context = {
            'profile': profile,
        }
        return render(request, 'user/profile.html', context)

@login_required
def edit_profile_view(request,username):
    if request.user.username != username:
        messages.error(request, "You do not have the right to modify this profile.")
        return redirect('user:edit_user_profile', username=username)

    profile = get_object_or_404(UserProfile,user=request.user)

    if request.method == "POST":
        form = ProfileUpdateForm(request.POST,
                                    request.FILES,
                                    instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('user:edit_user_profile', username=username)
    else:
        form = ProfileUpdateForm(instance=profile)

    context = {
        'form': form,
        'profile': profile
    }
    return render(request, 'user/edit_profile.html',context)

@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Prevents user from being logged out
            messages.success(request, 'Your password has been successfully updated!')
            return redirect('profile')
    else:
        form = PasswordChangeForm(user=request.user)
    return render(request, 'user/change_pwd.html', {'form': form})
# Create your views here.
