from django import forms
from .models import User

class ScoreInputForm(forms.Form):
    player_one = forms.ModelChoiceField(queryset=User.objects.all(), label="Player One")
    player_two = forms.ModelChoiceField(queryset=User.objects.all(), label="Player Two")