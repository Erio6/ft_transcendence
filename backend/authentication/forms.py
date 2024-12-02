from django import forms
from .models import UserProfile
from django.contrib.auth.models import User

# jai pas utiliser le user  update form mais je dois le mettre dans les updates views
class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()
    class Meta:
        model = User
        fields = ['username', 'email']

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['avatar','display_name']

class UserSearchForm(forms.Form):
    query = forms.CharField(max_length=100, required=False, widget=forms.TextInput(attrs={
        'placeholder': 'Looking for users...',
        'class': 'form-control',
    }))