# Generated by Django 4.0.4 on 2022-05-21 16:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0020_alter_track_audio_path'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='track',
            name='audio_path',
        ),
        migrations.AddField(
            model_name='track',
            name='audioFile',
            field=models.FileField(default=1, upload_to='uploads/'),
            preserve_default=False,
        ),
    ]