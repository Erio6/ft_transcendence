from django import forms
from .models import User

class ScoreInputForm(forms.Form):
    player_one = forms.ModelChoiceField(queryset=User.objects.all(), label="Player One")
    player_two = forms.ModelChoiceField(queryset=User.objects.all(), label="Player Two")
    player_one_score = forms.IntegerField(label="Player One Score", min_value=0)
    player_two_score = forms.IntegerField(label="Player Two Score", min_value=0)