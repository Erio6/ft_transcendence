# Generated by Django 5.1.3 on 2024-11-30 12:55

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('winner_score', models.IntegerField(default=0)),
                ('looser_score', models.IntegerField(default=0)),
                ('start_time', models.DateTimeField(auto_now_add=True)),
                ('end_time', models.DateTimeField(null=True)),
                ('looser', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='looser', to=settings.AUTH_USER_MODEL)),
                ('player_one', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='player_one', to=settings.AUTH_USER_MODEL)),
                ('player_two', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='player_two', to=settings.AUTH_USER_MODEL)),
                ('winner', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='winner', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
