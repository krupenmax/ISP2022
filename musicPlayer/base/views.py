from re import template
from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView
from django.urls import reverse_lazy
from .models import Track
# Create your views here.

class TrackList(ListView):
    model = Track
    context_object_name = 'tracks'

class TrackDetail(DetailView):
    model = Track
    context_object_name = 'track'
    template_name = 'base/track_detail.html'

class TrackCreate(CreateView):
    model = Track
    fields = '__all__'
    success_url = reverse_lazy('tracks')

class TrackUpdate(UpdateView):
    model = Track
    fields = '__all__'
    success_url = reverse_lazy('tracks')