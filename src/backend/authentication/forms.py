from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']

    # Optionally, you can add custom validation or help_text
    username = forms.CharField(
        help_text="Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only."
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput,
        help_text="Your password must contain at least 8 characters."
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput,
        help_text="Enter the same password as before, for verification."
    )
