import api.views as views
from django.conf.urls import url, include
from django.urls import path
from rest_framework import routers

urlpatterns = [
    path('video', views.VideoViewSet.as_view({'get': 'list'}), name='video'),
    url(r'^get_tag_count_rank$', views.get_tag_count_rank, name='get_tag_count_rank'),
]
