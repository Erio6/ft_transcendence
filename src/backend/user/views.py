from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import UserUpdateForm, ProfileUpdateForm
from django.contrib.auth.models import User
from .models import UserProfile
from django.contrib import messages
from django.shortcuts import render
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.conf import settings
@login_required(login_url='authentication:login')
def profile_view(request,username):
        user = get_object_or_404(User, username=username)
        profile = get_object_or_404(UserProfile, user=user)
        score = get_score(user.username)
        context = {
            'profile': profile,
            'score': score,
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
        form2 = UserUpdateForm(request.POST, instance=request.user)
        if form.is_valid() & form2.is_valid():
            form.save()
            form2.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('user:user_profile', username=username)
    else:
        form = ProfileUpdateForm(instance=profile)
        form2 = UserUpdateForm(instance=request.user)

    context = {
        'form': form,
        'form2': form2,
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
