# Generated by Django 4.0.4 on 2022-05-19 21:13

import audiofield.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0015_track_audio_path'),
    ]

    operations = [
        migrations.AlterField(
            model_name='track',
            name='audio_path',
            field=audiofield.fields.AudioField(upload_to='your/upload/dir'),
        ),
    ]