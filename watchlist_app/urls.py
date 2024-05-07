from django.urls import path
from watchlist_app.views import *

urlpatterns = [
    path('watchlist/', WatchListAV.as_view(), name='watchlist-list'),
    path('movie/<int:pk>/', WatchDetailDV.as_view(), name='watchlist-detail'),
    path('stream/', StreamingPlatformAV.as_view(), name='streaming-list'),
    path('stream/<int:pk>/', StreamingPlatformDV.as_view(), name='streaming-detail')
]
