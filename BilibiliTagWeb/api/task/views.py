from __future__ import unicode_literals
import base64
import json

from django.http import JsonResponse
from django.conf import settings

from api.helpers import *
from api.tasks import *
from BilibiliTagHandler.tag_handler import TagHandler
from BilibiliTagWeb.celery import app as celery_app
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

def get_running_list(request, *args, **kwargs):
    # queue_name = 'celery'

    # with celery_app.pool.acquire(block=True) as conn:
    #     tasks = conn.default_channel.client.lrange(queue_name, 0, -1)

    # decoded_tasks = []

    # for task in tasks:
    #     j = json.loads(task)
    #     body = json.loads(base64.b64decode(j['body']))
    #     decoded_tasks.append(body)
    tasks = celery_app.control.inspect().active()

    return JsonResponse(response_json({'tasks': tasks}, ''))