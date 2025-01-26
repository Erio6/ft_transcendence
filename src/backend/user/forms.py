from .models import UserProfile
from django.contrib.auth.models import User
from django import forms

# jai pas utiliser le user  update form mais je dois le mettre dans les updates views note pour Elo pour l update
class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()
    class Meta:
        model = User
        fields = ['username','email']

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['country']

class AvatarUpdateForm(forms.ModelForm):
    avatar = forms.ImageField(
        label='',  # Remove label
        widget=forms.FileInput(attrs={
            'class': 'hidden-input',
            'show_initial': False  # Don't show current file
        })
    )

    class Meta:
        model = UserProfile
        fields = ['avatar']
