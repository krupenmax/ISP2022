# Generated by Django 4.0.4 on 2022-05-19 21:13


from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0015_track_audio_path'),
    ]

    operations = [
        migrations.AlterField(
            model_name='track',
            name='audio_path',
            field=models.FileField(upload_to='your/upload/dir'),
        ),
    ]
