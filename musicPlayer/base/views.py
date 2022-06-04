from asyncio import events
from distutils.log import Log
from msilib.schema import EventMapping
from multiprocessing import Event
from re import search, template
from turtle import onkeypress
from django.shortcuts import redirect, render
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.views import View
from .models import Track
# Create your views here.

class CustomLoginView(LoginView):
    template_name = 'base/login.html'
    field = '__all__'   
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('tracks')


class RegisterView(FormView):
    template_name = 'base/register.html'
    form_class = UserCreationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('tracks')

    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request, user)
        return super(RegisterView, self).form_valid(form)

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('tracks')
        return super(RegisterView, self).get(*args, **kwargs)

class TrackList(LoginRequiredMixin, ListView):
    model = Track
    context_object_name = 'tracks'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        search_input = self.request.GET.get('search-area') or ''
        if search_input:
            context['tracks'] = context['tracks'].filter(title__icontains=search_input) | context['tracks'].filter(artist__icontains=search_input)
            context['search_input'] = search_input
        return context

class TrackDetail(LoginRequiredMixin, DetailView):
    model = Track
    context_object_name = 'track'
    template_name = 'base/track_detail.html'


class TrackCreate(LoginRequiredMixin, CreateView):
    model = Track
    fields = ['title', 'artist', 'genre', 'description']
    success_url = reverse_lazy('tracks')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(TrackCreate, self).form_valid(form)

class TrackUpdate(LoginRequiredMixin, UpdateView):
    model = Track
    fields = ['title', 'artist', 'genre', 'description']
    success_url = reverse_lazy('tracks')

class TrackDelete(LoginRequiredMixin, DeleteView):
    model = Track
    context_object_name = 'track'
    success_url = reverse_lazy('tracks')

class AboutSite(ListView):
    model = Track
    template_name = 'base/about.html'
