from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.shortcuts import redirect

def home(request):
    return render(request, 'djangoProject/home.html')