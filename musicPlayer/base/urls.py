from django.urls import path

from base.models import Track
from .views import TrackList

urlpatterns = [
     path('', TrackList.as_view(), name='Tracks'),
]
