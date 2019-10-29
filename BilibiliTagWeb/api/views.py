from __future__ import unicode_literals
from django_filters import rest_framework as filters
from rest_framework import viewsets
from rest_framework.filters import SearchFilter, OrderingFilter
from api.pagination import CustomPageNumberPagination
from rest_framework.response import Response
from api.serializers import *
from api.models import *


class VideoViewSet(viewsets.ModelViewSet):
    serializer_class = VideoSerializer
    pagination_class = CustomPageNumberPagination
    queryset = Videos.objects.all()
    filter_backends = (filters.DjangoFilterBackend,
                       SearchFilter, OrderingFilter)
    __basic_fields = ('tid',)
    filter_fields = __basic_fields
    # search_fields = __basic_fields
    ordering = 'pubdate'

    def __init__(self, **kwargs):
        super(VideoViewSet, self).__init__(**kwargs)

    def list(self, request, *args, **kwargs):
        response_data = super(VideoViewSet, self).list(
            request, *args, **kwargs)
        return Response(response_data.data)

    def retrieve(self, request, *args, **kwargs):
        response_data = super(VideoViewSet, self).retrieve(
            request, *args, **kwargs)
        return Response(response_data.data)

    # def get_queryset(self):
    #     return Videos.objects.all()

    # def list(self, request, *args, **kwargs):
    #     queryset = Videos.objects.all()
    #     response = {
    #         'code': 0,
    #         'data': [],
    #         'total': ''
    #     }
    #     serializer = self.serializer_class(queryset, many=True)
    #     response['data'] = self.serializer_class.data
    #     response['total'] = len(serializer.data)
    #     return Response(response)

# TODO: EmbeddedModelField对应的filter，已遗弃
# from copy import deepcopy
# from djongo.models import EmbeddedModelField
# from django.contrib.postgres.forms import SimpleArrayField
# from django_filters import filterset
# from django_filters.rest_framework.filters import Filter


# class EmbeddedFilter(Filter):
#     base_field_class = EmbeddedModelField


# class PostgresFieldFilterSet(filters.FilterSet):
#     FILTER_DEFAULTS = deepcopy(filterset.FILTER_FOR_DBFIELD_DEFAULTS)
#     FILTER_DEFAULTS.update({
#         EmbeddedModelField: {
#             'filter_class': EmbeddedFilter,
#         },
#     })


# class EmbeddedFilterBackend(filters.DjangoFilterBackend):
#     default_filter_set = PostgresFieldFilterSet
