from __future__ import unicode_literals

from django.http import JsonResponse
from django.conf import settings

from api.helpers import *
from BilibiliTagHandler.tag_handler import TagHandler
from helpers import *

def get_tag_count_rank(request):
    if not check_dict_required_param(request.GET, ['tid', 'from', 'to', 'count']):
        return JsonResponse(response_json({}, '缺少参数'))

    type_id = int(request.GET.get('tid'))
    time_from = int(request.GET.get('from'))
    time_to = int(request.GET.get('to'))
    count = int(request.GET.get('count'))

    time_from = date_to_timestamp(time_from)
    time_to_end = date_to_timestamp(time_to) + 24 * 3600

    mongo_settings = settings.DATABASES['default']
    handler = TagHandler(mongo_settings['HOST'],
                    mongo_settings['NAME'],
                    mongo_settings['USER'],
                    mongo_settings['PASSWORD'])
    data = {
        'result': handler.get_tag_count_rank(type_id, time_from, time_to_end, count)
    }
    return JsonResponse(response_json(data, ''))

def get_tag_avg_stat_rank(request):
    if not check_dict_required_param(request.GET, ['tid', 'from', 'to', 'count', 'stat_index', 'min_tag_count']):
        return JsonResponse(response_json({}, '缺少参数'))

    type_id = int(request.GET.get('tid'))
    time_from = int(request.GET.get('from'))
    time_to = int(request.GET.get('to'))
    count = int(request.GET.get('count'))
    stat_index = int(request.GET.get('stat_index'))
    min_tag_count = int(request.GET.get('min_tag_count'))

    time_from = date_to_timestamp(time_from)
    time_to_end = date_to_timestamp(time_to) + 24 * 3600

    mongo_settings = settings.DATABASES['default']
    handler = TagHandler(mongo_settings['HOST'],
                    mongo_settings['NAME'],
                    mongo_settings['USER'],
                    mongo_settings['PASSWORD'])
    data = {
        'result': handler.get_tag_avg_stat_rank(type_id, time_from, time_to_end, count, stat_index, min_tag_count)
    }
    return JsonResponse(response_json(data, ''))
