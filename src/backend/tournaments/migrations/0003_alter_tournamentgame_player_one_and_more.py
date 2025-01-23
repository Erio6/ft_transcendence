# Generated by Django 5.1.4 on 2025-01-15 14:15

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tournaments', '0002_alter_tournamentgame_round_number'),
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tournamentgame',
            name='player_one',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='tournament_player_one', to='user.userprofile'),
        ),
        migrations.AlterField(
            model_name='tournamentgame',
            name='player_two',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='tournament_player_two', to='user.userprofile'),
        ),
    ]
