# Generated by Django 4.0.4 on 2022-05-23 14:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0030_track_tracklist'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='track',
            name='tracklist',
        ),
    ]