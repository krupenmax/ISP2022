from ast import Delete
from django.urls import path

from base.models import Track, Genre
from .views import TrackCreate, TrackDetail, TrackList, TrackCreate, TrackUpdate, TrackDelete, CustomLoginView, RegisterView
from django.contrib.auth.views import LogoutView

urlpatterns = [
     path('login/', CustomLoginView.as_view(), name='login'),
     path('register/', RegisterView.as_view(), name='register'),
     path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
     path('', TrackList.as_view(), name='tracks'),
     path('track/<int:pk>/', TrackDetail.as_view(), name='track'),
     path('track-create/', TrackCreate.as_view(), name = "track-create"),
     path('track-update/<int:pk>/', TrackUpdate.as_view(), name = "track-update"),
     path('track-delete/<int:pk>/', TrackDelete.as_view(), name = "track-delete"),
     path('../musics/a.mp3', TrackDetail.as_view(), name = 'track-play')
]
