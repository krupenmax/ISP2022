# Generated by Django 4.0.4 on 2022-05-14 12:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0006_rename_genre_genre_trackgenre_alter_track_genre'),
    ]

    operations = [
        migrations.CreateModel(
            name='Genre_List',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.RenameField(
            model_name='genre',
            old_name='Trackgenre',
            new_name='Genre_Name',
        ),
        migrations.AlterField(
            model_name='track',
            name='genre',
            field=models.ManyToManyField(to='base.genre'),
        ),
    ]
