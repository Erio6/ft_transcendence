# Generated by Django 5.1.4 on 2025-01-14 15:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tournaments', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tournamentgame',
            name='round_number',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
