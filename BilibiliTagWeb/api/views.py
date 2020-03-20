from __future__ import unicode_literals
from BilibiliTagHandler.tag_handler import TagHandler, date_to_timestamp
from api.models import *
from api.pagination import CustomPageNumberPagination
from api.serializers import *
from django_filters import rest_framework as filters
from django.http import JsonResponse
from django.conf import settings
from rest_framework import viewsets
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.response import Response


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

def response_json(data, errmsg):
    result = {
        "status": 0,
        "data": data,
        "errors": [],
        "message": "success"
    }
    if errmsg != "":
        result["status"] = 1
        result["data"] = {}
        result["message"] = errmsg
    return result

def get_tag_count_rank(request):
    type_id = int(request.GET.get("tid"))
    time_from = str(request.GET.get("from"))
    time_to = str(request.GET.get("to"))
    count = int(request.GET.get("count"))
    if not type_id or not time_from or not time_to or not count:
        return JsonResponse(response_json({}, "缺少参数"))
    time_from = date_to_timestamp(time_from)
    time_to = date_to_timestamp(time_to) + 24 * 3600

    mongo_settings = settings.DATABASES['default']
    handler = TagHandler(mongo_settings['HOST'],
                    mongo_settings['NAME'],
                    mongo_settings['USER'],
                    mongo_settings['PASSWORD'])
    data = {
        "result": handler.get_tag_count_rank(type_id, time_from, time_to, count)
    }
    return JsonResponse(response_json(data, ""))
