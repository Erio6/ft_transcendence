from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

from .forms import UserUpdateForm, ProfileUpdateForm, AvatarUpdateForm
from django.contrib.auth.models import User
from .models import UserProfile
from django.contrib import messages
from django.shortcuts import render
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.conf import settings


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def edit_profile_view(request, username):
    if request.user.username != username:
        messages.error(request, "You do not have the right to modify this profile.")
        return redirect('user:edit_profile', username=username)

    profile = get_object_or_404(UserProfile, user=request.user)

    if request.method == "POST":
        form_type = request.POST.get('form_type')

        if form_type == 'avatar':
            avatar_form = AvatarUpdateForm(request.POST, request.FILES, instance=profile)
            if avatar_form.is_valid():
                avatar_form.save()
                messages.success(request, f'Your profile picture has been updated!')
                return redirect('user:edit_profile', username=request.user.username)
            else:
                form = ProfileUpdateForm(instance=profile)
                form2 = UserUpdateForm(instance=request.user)
                context = {
                    'form': form,
                    'form2': form2,
                    'avatar_form': avatar_form,
                    'profile': profile
                }

        elif form_type == 'profile_info':
            form = ProfileUpdateForm(request.POST,
                                     request.FILES,
                                     instance=profile)
            form2 = UserUpdateForm(request.POST or None, instance=request.user)
            if form.is_valid() & form2.is_valid():
                form.save()
                form2.save()
                messages.success(request, f'Your account has been updated!')
                return redirect('user:edit_profile', username=request.user.username)
            else:
                avatar_form = AvatarUpdateForm(instance=profile)
                context = {
                    'form': form,
                    'form2': form2,
                    'avatar_form': avatar_form,
                    'profile': profile
                }
        else:
            form = ProfileUpdateForm(instance=profile)
            avatar_form = AvatarUpdateForm(instance=profile)
            form2 = UserUpdateForm(instance=request.user)

            context = {
                'form': form,
                'form2': form2,
                'avatar_form': avatar_form,
                'profile': profile
            }

    else:
        # For GET requests, initialize the forms normally.
        form = ProfileUpdateForm(instance=profile)
        form2 = UserUpdateForm(instance=request.user)
        avatar_form = AvatarUpdateForm(instance=profile)
        context = {
            'form': form,
            'form2': form2,
            'avatar_form': avatar_form,
            'profile': profile
        }

    return render(request, 'user/edit_profile.html', context)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def change_password(request):
    profile = get_object_or_404(UserProfile, user=request.user)
    if request.method == 'POST':
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Prevents user from being logged out
            messages.success(request, 'Your password has been successfully updated!')
            return redirect('home')
    else:
        form = PasswordChangeForm(user=request.user)
    return render(request, 'user/change_pwd.html', {'form': form, 'profile': profile})
# Create your views here.
