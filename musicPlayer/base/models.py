from __future__ import generator_stop
from tkinter import CASCADE
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.

class Genre(models.Model):
    genre_name = models.CharField(max_length=256) 
    def __str__(self):
        return self.genre_name


class Track(models.Model):
    title = models.CharField(max_length=256)
    user = models.ManyToManyField(User)
    audioFile = models.FileField()
    artist = models.CharField(max_length=256)
    genre = models.ManyToManyField(Genre)
    description = models.TextField(null=True, blank=True)
    create = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    
    def get_path(self):
        return self.audioFile


