from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from .forms import UserUpdateForm, ProfileUpdateForm
from .models import Friendship, UserProfile
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
def profile_view(request):
    if request.method == "POST":
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST,
                                         request.FILES,
                                         instance=request.user.userprofile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('authentication:profile')
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.userprofile)

    context = {
        'user_form': user_form,
        'profile_form': profile_form
    }

    return render(request, 'authentication/profile.html',context)


@login_required
def friends_overview(request):
    user_profile = request.user.userprofile

    friendships_sent = user_profile.friendships_sent.filter(status='accepted')
    friendships_received = user_profile.friendships_received.filter(status='accepted')

    friends = [friendship.to_user for friendship in friendships_sent]
    friends += [friendship.from_user for friendship in friendships_received]

    incoming_requests = user_profile.friendships_received.filter(status='pending')
    outgoing_requests = user_profile.friendships_sent.filter(status='pending')

    context = {
        'friends': friends,
        'incoming_requests': incoming_requests,
        'outgoing_requests': outgoing_requests,
    }
    return render(request, 'authentication/friends.html', context)

@login_required
def send_friend_request(request, user_id):
    from_user = request.user.userprofile
    to_user = get_object_or_404(UserProfile, id=user_id)
    if from_user != to_user:
        friendship, created = Friendship.objects.get_or_create(
            from_user=from_user,
            to_user=to_user,
            defaults={'status': 'pending'}
        )
        if created:
            messages.success(request, f'Friend request sent to {to_user.user.username}')
        else:
            messages.success(request, f'Friend request already sent to {to_user.user.username}')
    else:
        messages.error(request, f'You cannot send a friend request to yourself')
    return redirect('authentication:friends')

@login_required
def respond_friend_request(request, friendship_id, action):
    friendship = get_object_or_404(Friendship, id=friendship_id, to_user=request.user.userprofile, status='pending')
    if action == 'accept':
        Friendship.status = 'accepted'
        Friendship.save()
        Friendship.objects.get_or_create(
            from_user=Friendship.to_user,
            to_user=Friendship.from_user,
            defaults={'status': 'accepted'}
        )
        messages.info(request, f'Friend request from {friendship.from_user.user.username} accepted')
    elif action == 'decline':
        Friendship.status = 'rejected'
        Friendship.save()
        messages.info(request, f'Friend request from {friendship.from_user.user.username} declined')
    return redirect('authentication:friends')

@login_required
def cancel_friend_request(request, friendship_id):
    Friendship = get_object_or_404(Friendship, id=friendship_id, from_user=request.user.userprofile, status='pending')
    Friendship.delete()
    messages.info(request, f'Friend request to {friendship.to_user.user.username} cancelled')
    return redirect('authentication:friends')

@login_required
def remove_friend(request, user_id):
    user_profile = request.user.userprofile
    friend_profile = get_object_or_404(UserProfile, id=user_id)
    Friendship.objects.filter(
        from_user=user_profile,
        to_user=friend_profile,
        status='accepted'
    ).delete()
    Friendship.objects.filter(
        from_user=friend_profile,
        to_user=user_profile,
        status='accepted'
    ).delete()
    messages.info(request, f'{friend_profile.user.username} removed from friends')
    return redirect('authentication:friends')
