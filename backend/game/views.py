from django.shortcuts import render
from django.shortcuts import redirect

def welcome(request):
    return render(request, 'game/welcome.html')