# Generated by Django 4.0.4 on 2022-05-16 20:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0011_genre_remove_track_genre_track_genre'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='track',
            name='genre',
        ),
        migrations.AddField(
            model_name='track',
            name='genre',
            field=models.ForeignKey(default=4, on_delete=django.db.models.deletion.CASCADE, to='base.genre'),
            preserve_default=False,
        ),
    ]