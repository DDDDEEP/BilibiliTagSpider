from __future__ import unicode_literals

from api.models import Videos, Records
from api.pagination import CustomPageNumberPagination
from api.serializers import VideoSerializer, RecordSerializer
from django_filters import rest_framework as filters
from rest_framework import viewsets
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.response import Response


class VideoViewSet(viewsets.ModelViewSet):
    serializer_class = VideoSerializer
    pagination_class = CustomPageNumberPagination
    queryset = Videos.objects.all()
    filter_backends = (filters.DjangoFilterBackend, SearchFilter,
                       OrderingFilter)
    __basic_fields = ('tid', )
    filter_fields = __basic_fields
    # search_fields = __basic_fields
    ordering = 'pubdate'

    def __init__(self, **kwargs):
        super(VideoViewSet, self).__init__(**kwargs)

    def list(self, request, *args, **kwargs):
        response_data = super(VideoViewSet, self).list(request, *args,
                                                       **kwargs)
        return Response(response_data.data)

    def retrieve(self, request, *args, **kwargs):
        response_data = super(VideoViewSet,
                              self).retrieve(request, *args, **kwargs)
        return Response(response_data.data)


class RecordViewSet(viewsets.ModelViewSet):
    serializer_class = RecordSerializer
    pagination_class = CustomPageNumberPagination
    queryset = Records.objects.all()
    filter_backends = (filters.DjangoFilterBackend, SearchFilter,
                       OrderingFilter)
    __basic_fields = ('tid', )
    filter_fields = __basic_fields
    # search_fields = __basic_fields
    ordering = 'pubdate'

    def __init__(self, **kwargs):
        super(RecordViewSet, self).__init__(**kwargs)

    def list(self, request, *args, **kwargs):
        response_data = super(RecordViewSet,
                              self).list(request, *args, **kwargs)
        return Response(response_data.data)

    def retrieve(self, request, *args, **kwargs):
        response_data = super(RecordViewSet,
                              self).retrieve(request, *args, **kwargs)
        return Response(response_data.data)
