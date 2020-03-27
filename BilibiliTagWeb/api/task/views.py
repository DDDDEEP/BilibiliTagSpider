from __future__ import unicode_literals

from django.http import JsonResponse
from django.conf import settings

from api.helpers import *
from api.tasks import *
from BilibiliTagHandler.tag_handler import TagHandler
from celery.result import AsyncResult
from celery_once import AlreadyQueued
from helpers import *

def start_handler(request, *args, **kwargs):
    if not check_dict_required_param(request.GET, ['tid', 'from', 'to']):
        return JsonResponse(response_json({}, '缺少参数'))

    type_id = int(request.GET.get('tid'))
    time_from = int(request.GET.get('from'))
    time_to = int(request.GET.get('to'))
    
    time_from = date_to_timestamp(time_from)
    time_to_end = date_to_timestamp(time_to) + 24 * 3600

    try:
        task = task_handler.delay(type_id, time_from, time_to_end)
    except AlreadyQueued:
        return JsonResponse(response_json({}, '仍有处理任务执行中'))
    else:
        return JsonResponse(response_json({'task_id': task.id, 'task_state': task.state}, ''))

def get_handler_progress(request, *args, **kwargs):
    task_id = request.GET.get('task_id', None)
    if task_id is not None:
        task = AsyncResult(task_id)
        data = {
            'state': task.state,
            'result': task.result,
        }
        return JsonResponse(response_json(data, ''))
    else:
        return JsonResponse(response_json({}, '缺少参数'))

def start_spider(request, *args, **kwargs):
    if not check_dict_required_param(request.GET, ['tid', 'from', 'to']):
        return JsonResponse(response_json({}, '缺少参数'))

    type_id = int(request.GET.get('tid'))
    time_from = int(request.GET.get('from'))
    time_to = int(request.GET.get('to'))
    
    time_from = date_to_timestamp(time_from)
    time_to_end = date_to_timestamp(time_to) + 24 * 3600

    try:
        task = task_spider.delay(type_id, time_from, time_to_end)
    except AlreadyQueued:
        return JsonResponse(response_json({}, '仍有爬虫任务执行中'))
    else:
        return JsonResponse(response_json({'task_id': task.id, 'task_state': task.state}, ''))

def get_spider_progress(request, *args, **kwargs):
    task_id = request.GET.get('task_id', None)
    if task_id is not None:
        task = AsyncResult(task_id)
        data = {
            'state': task.state,
            'result': task.result,
        }
        return JsonResponse(response_json(data, ''))
    else:
        return JsonResponse(response_json({}, '缺少参数'))