# Generated by Django 5.1.4 on 2025-01-08 11:03

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tournament',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('start_date', models.DateTimeField()),
                ('end_date', models.DateTimeField(null=True)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tournament_creator', to='user.userprofile')),
            ],
        ),
        migrations.CreateModel(
            name='TournamentGame',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('player_one_score', models.IntegerField(default=0)),
                ('player_two_score', models.IntegerField(default=0)),
                ('winner_score', models.IntegerField(default=0)),
                ('looser_score', models.IntegerField(default=0)),
                ('start_time', models.DateTimeField(auto_now_add=True)),
                ('end_time', models.DateTimeField(null=True)),
                ('is_completed', models.BooleanField(default=False)),
                ('looser', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tournament_game_looser', to='user.userprofile')),
                ('player_one', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tournament_player_one', to='user.userprofile')),
                ('player_two', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tournament_player_two', to='user.userprofile')),
                ('tournament', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tournaments.tournament')),
                ('winner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tournament_game_winner', to='user.userprofile')),
            ],
        ),
        migrations.CreateModel(
            name='TournamentPlayer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('score', models.IntegerField(default=0)),
                ('player', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.userprofile')),
                ('tournament', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tournaments.tournament')),
                ('winner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tournament_winner', to='user.userprofile')),
            ],
        ),
        migrations.AddField(
            model_name='tournament',
            name='players',
            field=models.ManyToManyField(through='tournaments.TournamentPlayer', to='tournaments.tournament'),
        ),
    ]
