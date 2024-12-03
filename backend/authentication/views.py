from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from .forms import UserUpdateForm, ProfileUpdateForm
from django.contrib.auth.models import User
from .models import UserProfile, FriendList , FriendRequest
from django.contrib import messages
from django.db.models import Q

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
        return redirect('authentication:edit_user_profile', username=username)

    profile = get_object_or_404(UserProfile,user=request.user)

    if request.method == "POST":
        form = ProfileUpdateForm(request.POST,
                                    request.FILES,
                                    instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('authentication:edit_user_profile', username=username)
    else:
        form = ProfileUpdateForm(instance=profile)

    context = {
        'form': form,
        'profile': profile
    }
    return render(request, 'authentication/edit_profile.html',context)

# FRIENDS VIEWS

@login_required
def friends_overview(request):
    user_profile = get_object_or_404(UserProfile, user=request.user)
    friends = user_profile.friend_list.friends.all()
    incoming_requests = FriendRequest.objects.filter(receiver=user_profile, status='Pending')
    outgoing_requests = FriendRequest.objects.filter(sender=user_profile, status='Pending')

    query = request.GET.get('q', '')
    search_results = []
    if query:
        search_results = UserProfile.objects.filter(
            user__username__icontains=query
        ).exclude(
            user=request.user
        ).exclude(
            Q(friend_list__friends=user_profile) |
            Q(receiver__sender=user_profile, receiver__status='pending') |
            Q(sender__receiver=user_profile, sender__status='pending')
        ).distinct()

    context = {
        'friends': friends,
        'incoming_requests': incoming_requests,
        'outgoing_requests': outgoing_requests,
        'search_results': search_results,
        'query': query,
    }
    return render(request, 'authentication/friends.html', context)


@login_required
def send_friend_request(request, user_id):
    if request.method == 'POST':
        sender = get_object_or_404(UserProfile, user=request.user)
        receiver = get_object_or_404(UserProfile, id=user_id)

        if sender == receiver:
            messages.error(request, "You cannot sent a friend request.")
            return redirect('authentication:friends_overview')

        existing_request = FriendRequest.objects.filter(
            sender=sender, receiver=receiver, status='Pending'
        ).exists()

        existing_friendship = FriendList.objects.filter(
            Q(user_profile=sender, friends=receiver) | Q(user_profile=receiver, friends=sender)
        ).exists()

        if existing_request:
            messages.info(request, "Friend request is pending.")
        elif existing_friendship:
            messages.info(request, "Your are already friends")
        else:
            FriendRequest.objects.create(sender=sender, receiver=receiver)
            messages.success(request, f'Friend request sent to {receiver.display_name}.')

    return redirect('authentication:friends_overview')


@login_required
def accept_friend_request(request, request_id):
    friend_request = get_object_or_404(FriendRequest, id=request_id, receiver__user=request.user, status='Pending')
    if request.method == 'POST':
        friend_request.accept()
        messages.success(request, f'You are now friend with {friend_request.sender.display_name}.')
    return redirect('authentication:friends_overview')


@login_required
def decline_friend_request(request, request_id):
    friend_request = get_object_or_404(FriendRequest, id=request_id, receiver__user=request.user, status='Pending')
    if request.method == 'POST':
        friend_request.decline()
        messages.info(request, f'Friend request sent to{friend_request.sender.display_name} declined.')
    return redirect('authentication:friends_overview')

@login_required
def cancel_friend_request(request, request_id):
    friend_request = get_object_or_404(FriendRequest, id=request_id, sender__user=request.user, status='Pending')
    if request.method == 'POST':
        friend_request.cancel()
        messages.info(request, f'Friend request sent to {friend_request.receiver.display_name} cancelled.')
    return redirect('authentication:friends_overview')

@login_required
def remove_friend(request, friend_id):
    friend = get_object_or_404(UserProfile, id=friend_id)
    friend_list = get_object_or_404(FriendList, user_profile__user=request.user)
    if request.method == 'POST':
        friend_list.remove_friend(friend)
        other_friend_list = get_object_or_404(FriendList, user_profile=friend)
        other_friend_list.remove_friend(friend_list.user_profile)
        messages.info(request, f'Friend {friend.display_name} Deleted.')
    return redirect('authentication:friends_overview')

