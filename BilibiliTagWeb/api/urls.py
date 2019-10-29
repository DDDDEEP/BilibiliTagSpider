from django.conf.urls import url, include
from django.urls import path
from api.views import VideoViewSet
from rest_framework import routers

urlpatterns = [
    path('video', VideoViewSet.as_view({'get': 'list'}), name='video'),
]
