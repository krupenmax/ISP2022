# Generated by Django 4.0.4 on 2022-05-12 20:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0002_track_delete_task'),
    ]

    operations = [
        migrations.AlterField(
            model_name='track',
            name='genre',
            field=models.CharField(choices=[('Рэп', 'Рэп '), ('Классика', 'Классика')], max_length=256),
        ),
    ]