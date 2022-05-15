from django.urls import path

from base.models import Track
from .views import TrackCreate, TrackDetail, TrackList, TrackCreate, TrackUpdate

urlpatterns = [
     path('', TrackList.as_view(), name='tracks'),
     path('track/<int:pk>/', TrackDetail.as_view(), name='track'),
     path('track-create/', TrackCreate.as_view(), name = "track-create"),
     path('track-update/<int:pk>/', TrackUpdate.as_view(), name = "track-update")
]
