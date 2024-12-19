from .models import UserProfile
from django.contrib.auth.models import User
from django import forms

# jai pas utiliser le user  update form mais je dois le mettre dans les updates views note pour Elo pour l update
class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()
    class Meta:
        model = User
        fields = ['email']

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['avatar','display_name', 'country']
