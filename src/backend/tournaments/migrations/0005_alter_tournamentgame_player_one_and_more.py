# Generated by Django 5.1.3 on 2025-01-17 12:24

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tournaments', '0004_tournamentgame_parent'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tournamentgame',
            name='player_one',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='tournament_player_one', to='tournaments.tournamentplayer'),
        ),
        migrations.AlterField(
            model_name='tournamentgame',
            name='player_two',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='tournament_player_two', to='tournaments.tournamentplayer'),
        ),
        migrations.AlterField(
            model_name='tournamentgame',
            name='winner',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='game_winner', to='tournaments.tournamentplayer'),
        ),
    ]
