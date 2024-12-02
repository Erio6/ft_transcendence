from django.shortcuts import render, HttpResponse

def home(request):
    return render(request, "djangoProject/home.html")
