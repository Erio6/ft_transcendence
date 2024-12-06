# Generated by Django 5.1.3 on 2024-12-05 12:29

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tournaments', '0001_initial'),
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tournament',
            name='players',
            field=models.ManyToManyField(through='tournaments.TournamentPlayer', to='user.userprofile'),
        ),
        migrations.AlterField(
            model_name='tournamentplayer',
            name='player',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.userprofile'),
        ),
    ]
