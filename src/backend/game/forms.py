from django import forms
from .models import Game
from user.models import UserProfile


class GameCreationForm(forms.Form):
    # player_side = forms.ChoiceField(choices=[(1, "Player One (Left)"), (2, "Player Two (Right)")], label="Choose Your Side", widget=forms.RadioSelect)
    game_type = forms.ChoiceField(
        choices=[('solo_IA_easy', 'Easy IA'), ('solo_IA_medium', 'Medium IA'), ('solo_IA_hard', 'Hard IA'),
                 ('solo_player', 'Player 2')], label="Choose Your Game Type", widget=forms.Select)
