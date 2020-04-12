from __future__ import unicode_literals

from django_filters import rest_framework as filters
from rest_framework import viewsets
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.response import Response

from api.models import Videos, Records, Tags
from api.pagination import CustomPageNumberPagination
from api.serializers import VideoSerializer, RecordSerializer, TagSerializer


class VideoFilter(filters.FilterSet):
    tid = filters.NumberFilter()
    aid = filters.NumberFilter()
    pubdate = filters.RangeFilter()

    class Meta:
        model = Videos
        fields = ['tid', 'aid', 'pubdate']


class VideoViewSet(viewsets.ModelViewSet):
    serializer_class = VideoSerializer
    pagination_class = CustomPageNumberPagination
    queryset = Videos.objects.all()
    filter_backends = (filters.DjangoFilterBackend, SearchFilter,
                       OrderingFilter)
    filter_class = VideoFilter
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


class RecordFilter(filters.FilterSet):
    tid = filters.NumberFilter()
    pubdate = filters.RangeFilter()

    class Meta:
        model = Records
        fields = ['tid', 'pubdate']


class RecordViewSet(viewsets.ModelViewSet):
    serializer_class = RecordSerializer
    pagination_class = CustomPageNumberPagination
    queryset = Records.objects.all()
    filter_backends = (filters.DjangoFilterBackend, SearchFilter,
                       OrderingFilter)
    filter_class = RecordFilter
    __basic_fields = (
        'tid',
        'pubdate',
    )
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


class TagViewSet(viewsets.ModelViewSet):
    serializer_class = TagSerializer
    pagination_class = CustomPageNumberPagination
    queryset = Tags.objects.all()
    filter_backends = (filters.DjangoFilterBackend, SearchFilter,
                       OrderingFilter)
    # filter_class = RecordFilter
    __basic_fields = (
        'name',
    )
    filter_fields = __basic_fields
    # search_fields = __basic_fields

    def __init__(self, **kwargs):
        super(TagViewSet, self).__init__(**kwargs)

    def list(self, request, *args, **kwargs):
        response_data = super(TagViewSet,
                              self).list(request, *args, **kwargs)
        return Response(response_data.data)

    def retrieve(self, request, *args, **kwargs):
        response_data = super(TagViewSet,
                              self).retrieve(request, *args, **kwargs)
        return Response(response_data.data)
