from django.urls import path, include
from watchlist_app.views import *
from rest_framework.routers import DefaultRouter



router = DefaultRouter()
router.register('stream', StreamingPlatformVS, basename="streamplatform")

urlpatterns = [
    path('watchlist/', WatchListAV.as_view(), name='watchlist-list'),
    path('watchlist/<int:pk>/', WatchDetailDV.as_view(), name='watchlist-detail'),
    path('<int:pk>/review-create', ReviewCreate.as_view(), name='review-create'),
    path('<int:pk>/review', ReviewList.as_view(), name='review-list'),
    path('review/<int:pk>', ReviewDetail.as_view(), name='review-detail'),
    path('',include(router.urls))
]
