# Generated by Django 5.1.3 on 2024-12-05 12:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='playerprofile',
            name='user',
        ),
    ]
