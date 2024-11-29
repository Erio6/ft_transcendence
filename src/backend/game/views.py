from django.shortcuts import render

def welcome(request):
    return render(request, 'game/welcome.html', context={"name": "Anthony"})