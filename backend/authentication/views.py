from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django_otp import devices_for_user

"""from .forms import UserRegistrationForm"""
from django.contrib.auth.views import LoginView

def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            login(request,form.save())
            return redirect("two_factor:login")
    else:
        form = UserCreationForm()
    return render(request, "authentication/register.html", {"form": form})

def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            if devices_for_user(user, confirmed=True):
                return redirect('two_factor:profile')
            #login(request,user)
            return redirect("game:welcome")
    else:
        form = AuthenticationForm()
    return render(request, "authentication/login.html", {"form": form})


"""def register(request):
    if request.method == 'POST':
        form =  UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            login(request, user)
            return redirect('authentication/login.html')
    else:
        form = UserRegistrationForm()
    return render(request, 'authentication/register.html',{'form': form})

class LoginView(LoginView):
    template_name ="authentication/login.html"
    redirected_authenticated_user = True"""
