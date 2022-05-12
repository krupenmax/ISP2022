from django.shortcuts import render
from django.views.generic.list import ListView
from .models import Track
# Create your views here.

class TrackList(ListView):
    model = Track
    context_object_name = "Tracks"

    