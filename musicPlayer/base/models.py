from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Track(models.Model):
    Genre_List = (
        ('Рэп', 'Рэп '),
        ('Классика', 'Классика'),
    )
    title = models.CharField(max_length=256)
    artist = models.CharField(max_length=256)
    genre = models.CharField(max_length=256, choices=(Genre_List))
    description = models.TextField(null=True, blank=True)
    create = models.DateTimeField(auto_now_add=True)

def __str__(self):
    return self.title

class Meta:
    ordering = ['complete']
