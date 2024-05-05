from watchlist_app.views import *
from django.urls import path, include

urlpatterns = [
    path('list/', movie_list, name='list'),
    path('detail/<int:pk>/', movie_detail, name='detail'),
]