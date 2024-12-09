# Generated by Django 5.1.3 on 2024-12-09 14:00

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('user', '0003_remove_userprofile_draws_remove_userprofile_losses_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='GameHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('game_id', models.PositiveIntegerField()),
                ('date_played', models.DateTimeField(auto_now_add=True)),
                ('game_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contenttypes.contenttype')),
            ],
        ),
        migrations.CreateModel(
            name='Leaderboard',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total_points', models.IntegerField(default=0)),
                ('total_wins', models.PositiveIntegerField(default=0)),
                ('total_losses', models.PositiveIntegerField(default=0)),
                ('player', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='leaderboard', to='user.userprofile')),
            ],
        ),
    ]
