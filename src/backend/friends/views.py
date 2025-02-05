from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

from .models import FriendRequest, FriendList
from django.contrib import messages
from django.shortcuts import render
from django.db.models import Q
from user.models import UserProfile


# Create your views here.

@api_view(["GET","POST"])
@permission_classes([IsAuthenticated])
def friends_overview(request):
    userprofile = request.user.userprofile
    friend_list = get_object_or_404(FriendList, user=userprofile)
    friends = friend_list.friends.all()
    incoming_requests = FriendRequest.objects.filter(receiver=userprofile, status='Pending')
    outgoing_requests = FriendRequest.objects.filter(sender=userprofile, status='Pending')

    query = request.GET.get('q', '')
    search_results = []
    if query:
        search_results = UserProfile.objects.filter(
            user__username__icontains=query
        ).exclude(
            id=userprofile.id
        ).exclude(
            Q(friend_list__friends=userprofile) |
            Q(receiver__sender=userprofile, receiver__status='pending') |
            Q(sender__receiver=userprofile, sender__status='pending')
        ).distinct()
    profile = None
    if request.user.is_authenticated:
        profile = UserProfile.objects.get(user=request.user)

    context = {
        'friends': friends,
        'incoming_requests': incoming_requests,
        'outgoing_requests': outgoing_requests,
        'search_results': search_results,
        'query': query,
        'profile': profile,
    }
    return render(request, 'friends/friends.html', context)


@api_view(["GET","POST"])
@permission_classes([IsAuthenticated])
def send_friend_request(request, user_id):
    if request.method == 'POST':
        sender = request.user.userprofile
        receiver = get_object_or_404(UserProfile, id=user_id)

        if sender == receiver:
            messages.error(request, "You cannot sent a friend request.")
            return redirect('friends:friends_overview')

        existing_request = FriendRequest.objects.filter(
            sender=sender, receiver=receiver, status='Pending'
        ).exists()

        existing_friendship = FriendList.objects.filter(
            Q(user=sender, friends=receiver) | Q(user=receiver, friends=sender)
        ).exists()

        if existing_request:
            messages.info(request, "Friend request is pending.")
        elif existing_friendship:
            messages.info(request, "Your are already friends")
        else:
            FriendRequest.objects.create(sender=sender, receiver=receiver)
            messages.success(request, f'Friend request sent to {receiver.user.username}.')

    return redirect('friends:friends_overview')


@api_view(["GET","POST"])
@permission_classes([IsAuthenticated])
def accept_friend_request(request, request_id):
    friend_request = get_object_or_404(FriendRequest, id=request_id, receiver=request.user.userprofile,
                                       status='Pending')
    if request.method == 'POST':
        friend_request.accept()
        messages.success(request, f'You are now friend with {friend_request.sender.user.userprofile}.')
    return redirect('friends:friends_overview')


@api_view(["GET","POST"])
@permission_classes([IsAuthenticated])
def decline_friend_request(request, request_id):
    friend_request = get_object_or_404(FriendRequest, id=request_id, receiver=request.user.userprofile,
                                       status='Pending')
    if request.method == 'POST':
        friend_request.decline()
        messages.info(request, f'Friend request sent to{friend_request.sender.user.userprofile} declined.')
    return redirect('friends:friends_overview')


@api_view(["GET","POST"])
@permission_classes([IsAuthenticated])
def cancel_friend_request(request, request_id):
    friend_request = get_object_or_404(FriendRequest, id=request_id, sender=request.user.userprofile, status='Pending')
    if request.method == 'POST':
        friend_request.cancel()
        messages.info(request, f'Friend request sent to {friend_request.receiver.user.userprofile} cancelled.')
    return redirect('friends:friends_overview')


@api_view(["GET","POST"])
@permission_classes([IsAuthenticated])
def remove_friend(request, friend_id):
    friend = get_object_or_404(UserProfile, id=friend_id)
    friend_list = get_object_or_404(FriendList, user=request.user.userprofile)
    if request.method == 'POST':
        friend_list.remove_friend(friend)
        other_friend_list = get_object_or_404(FriendList, user=friend)
        other_friend_list.remove_friend(friend_list.user)
        messages.info(request, f'Friend {friend.user.userprofile} Deleted.')
    return redirect('friends:friends_overview')
