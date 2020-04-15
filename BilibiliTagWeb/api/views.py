from __future__ import unicode_literals

from django_filters import rest_framework as filters
from rest_framework import viewsets
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.response import Response
from rest_framework.decorators import action

from api.models import Videos, Records, Tags, VideoTag
from api.pagination import CustomPageNumberPagination
from api.serializers import VideoSerializer, RecordSerializer, TagSerializer, VideoTagSerializer
from api.helpers import check_dict_required_param


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
    ordering_fields = ['tid', 'pubdate']

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

    @action(detail=True, name='list_by_tag')
    def list_by_tag(self, request, *args, **kwargs):
        videos = Videos.objects.none()
        if check_dict_required_param(request.GET,
                                     ['tid', 'tag_pubdate', 'tag_name']):
            tag = Tags.objects.filter(name=request.GET.get('tag_name')).first()
            if tag is not None:
                videotag = VideoTag.objects.filter(
                    tid=request.GET.get('tid'),
                    pubdate=request.GET.get('tag_pubdate'),
                    tag_id=tag._id).first()
                if videotag is not None:
                    # videos = Videos.objects.filter(videotag.aids, field_name='aid')
                    videos = Videos.objects.filter(aid__in=videotag.aids)

        page = self.paginate_queryset(videos)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(videos, many=True)
        return Response(serializer.data)


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
    ordering_fields = ['tid', 'pubdate']

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
    __basic_fields = ('name', )
    filter_fields = __basic_fields

    # search_fields = __basic_fields

    def __init__(self, **kwargs):
        super(TagViewSet, self).__init__(**kwargs)

    def list(self, request, *args, **kwargs):
        response_data = super(TagViewSet, self).list(request, *args, **kwargs)
        return Response(response_data.data)

    def retrieve(self, request, *args, **kwargs):
        response_data = super(TagViewSet,
                              self).retrieve(request, *args, **kwargs)
        return Response(response_data.data)


class VideoTagFilter(filters.FilterSet):
    def filter_tag(self, queryset, value, *args, **kwargs):
        tag = Tags.objects.filter(name=args[0]).first()
        if tag is None:
            return VideoTag.objects.none()
        else:
            return queryset.filter(tag_id=tag._id)

    tid = filters.NumberFilter()
    pubdate = filters.RangeFilter()
    tag_id = filters.CharFilter(method='filter_tag')

    class Meta:
        model = VideoTag
        fields = ['tid', 'pubdate', 'tag_id']


class VideoTagViewSet(viewsets.ModelViewSet):
    serializer_class = VideoTagSerializer
    pagination_class = CustomPageNumberPagination
    queryset = VideoTag.objects.all()
    filter_backends = (filters.DjangoFilterBackend, SearchFilter,
                       OrderingFilter)
    filter_class = VideoTagFilter
    __basic_fields = (
        'tid',
        'pubdate',
        'tag_id',
    )
    filter_fields = __basic_fields
    # search_fields = __basic_fields
    ordering_fields = ['tid', 'pubdate', 'tag_id']

    def __init__(self, **kwargs):
        super(VideoTagViewSet, self).__init__(**kwargs)

    def list(self, request, *args, **kwargs):
        response_data = super(VideoTagViewSet,
                              self).list(request, *args, **kwargs)
        return Response(response_data.data)

    def retrieve(self, request, *args, **kwargs):
        response_data = super(VideoTagViewSet,
                              self).retrieve(request, *args, **kwargs)
        return Response(response_data.data)
