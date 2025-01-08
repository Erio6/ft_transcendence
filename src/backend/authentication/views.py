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
from rest_framework_simplejwt.tokens import RefreshToken
from django.http import JsonResponse
from django.urls import reverse
from django.http import HttpResponseRedirect
from two_factor.utils import default_device
import json

class CustomLoginView(LoginView):
    def form_valid(self, form):
        user = form.get_user()
        if default_device(user):
            return super().form_valid(form)
        else:
            return self.generate_jwt_response(user)

    def done(self, form_list, **kwargs):
        user = self.get_user()
        return self.generate_jwt_response(user)

    def generate_jwt_response(self, user):
        refresh = RefreshToken.for_user(user)
        return JsonResponse({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        })

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            if default_device(user):
                # User has 2FA enabled, redirect to 2FA verification
                return redirect('two_factor:login')
            else:
                # User doesn't have 2FA, log them in and generate JWT
                login(request, user)
                refresh = RefreshToken.for_user(user)
                return JsonResponse({
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                })
    return redirect('two_factor:login')

def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            # Generate JWT tokens
            refresh = RefreshToken.for_user(user)
            data = {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }

            # Option 1: Set JWT tokens as cookies (Secure, HttpOnly)
            response = HttpResponseRedirect(reverse('two_factor:setup'))
            response.set_cookie('jwt_tokens', json.dumps(data), httponly=True, secure=True)
            
            return response
    else:
        form = UserCreationForm()
    return render(request, "authentication/register.html", {"form": form})


@api_view(['POST'])
def logout_view(request):
    try:
        refresh_token = request.data["refresh_token"]
        token = RefreshToken(refresh_token)
        token.blacklist()
        logout(request)
        return redirect('home')
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)