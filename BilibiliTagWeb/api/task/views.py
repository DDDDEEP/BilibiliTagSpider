from __future__ import unicode_literals
import time

from celery.result import AsyncResult
from celery_once import AlreadyQueued
from django.core.paginator import Paginator
from django.http import JsonResponse

from api.tasks import task_handler, task_spider
from api.helpers import check_dict_required_param, response_json
from api.models import Tasks
from helpers import ScrapyField, HandlerField, TaskType


def start_handler(request, *args, **kwargs):
    if request.method != 'POST':
        return JsonResponse(response_json(errmsg='非POST请求'))
    if not check_dict_required_param(request.POST, ['tid', 'from', 'to']):
        return JsonResponse(response_json(errmsg='缺少参数'))

    type_id = int(request.POST.get('tid'))
    time_from = int(request.POST.get('from'))
    time_to = int(request.POST.get('to'))

    try:
        task = task_handler.delay(type_id, time_from, time_to)
    except AlreadyQueued:
        return JsonResponse(response_json(errmsg='仍有处理任务执行中'))
    else:
        Tasks.objects.create(task_id=task.id,
                             task_type=TaskType.Handler.value,
                             tid=type_id,
                             time_from=time_from,
                             time_to=time_to,
                             time_start=int(time.time()),
                             time_end=-1)
        return JsonResponse(
            response_json({
                'task_id': task.id,
                'task_state': task.state
            }, ''))


def get_handler_progress(request, *args, **kwargs):
    task_id = request.GET.get('task_id', None)
    if task_id is not None:
        task = AsyncResult(task_id)
        data = {
            'state': task.state,
            'result': task.result,
        }
        return JsonResponse(response_json(data))
    else:
        return JsonResponse(response_json(errmsg='缺少参数'))


def start_spider(request, *args, **kwargs):
    if request.method != 'POST':
        return JsonResponse(response_json(errmsg='非POST请求'))

    if not check_dict_required_param(request.POST, ['tid', 'from', 'to']):
        return JsonResponse(response_json(errmsg='缺少参数'))

    type_id = int(request.POST.get('tid'))
    time_from = int(request.POST.get('from'))
    time_to = int(request.POST.get('to'))

    try:
        task = task_spider.delay(type_id, time_from, time_to)
    except AlreadyQueued:
        return JsonResponse(response_json(errmsg='仍有爬虫任务执行中'))
    else:
        Tasks.objects.create(task_id=task.id,
                             task_type=TaskType.Scrapy.value,
                             tid=type_id,
                             time_from=time_from,
                             time_to=time_to,
                             time_start=int(time.time()),
                             time_end=-1)
        return JsonResponse(
            response_json({
                'task_id': task.id,
                'task_state': task.state
            }))


def get_spider_progress(request, *args, **kwargs):
    task_id = request.GET.get('task_id', None)
    if task_id is not None:
        task = AsyncResult(task_id)
        data = {
            'state': task.state,
            'result': task.result,
        }
        return JsonResponse(response_json(data))
    else:
        return JsonResponse(response_json(errmsg='缺少参数'))


def get_task_list(request, *args, **kwargs):
    """
    返回的json实例：
        {
            'task_type': 0,  # 0为爬虫，1为处理器
            'tid': 17,
            'time_from': 20160101,
            'time_to': 20160101,
            'time_start': 1585321895,
            'time_end': -1,
            'state': 'PROGRESS',
            'progress': [
                {
                    'cur': 100,
                    'total': 7000
                },
                {
                    'cur': 0,
                    'total': 0
                }
            ],
            'extra': {}
        }
    """
    if not check_dict_required_param(request.GET, ['pageIndex', 'pageSize']):
        return JsonResponse(response_json(errmsg='缺少参数'))

    pageIndex = int(request.GET.get('pageIndex'))
    pageSize = int(request.GET.get('pageSize'))

    queryset = Tasks.objects.all().order_by('-time_start')
    task_records = Paginator(queryset, pageSize).page(pageIndex)

    result = []
    for task_record in task_records:
        celery_task = AsyncResult(task_record.task_id)
        item = {
            'task_type': task_record.task_type,
            'tid': task_record.tid,
            'time_from': task_record.time_from,
            'time_to': task_record.time_to,
            'time_start': task_record.time_start,
            'time_end': task_record.time_end,
            'state': celery_task.state,
            'progress': [],
            'extra': {},
        }


        if celery_task.state == 'PROGRESS' or celery_task.state == 'SUCCESS':
            if (task_record.task_type == TaskType.Scrapy.value):
                item['progress'].append({
                    'cur':
                    celery_task.result[ScrapyField.VideoCur.value],
                    'total':
                    celery_task.result[ScrapyField.VideoTotal.value],
                })
            elif (task_record.task_type == TaskType.Handler.value):
                item['progress'].append({
                    'cur':
                    celery_task.result[HandlerField.HandleCur.value],
                    'total':
                    celery_task.result[HandlerField.HandleTotal.value],
                })
                item['progress'].append({
                    'cur':
                    celery_task.result[HandlerField.CalCur.value],
                    'total':
                    celery_task.result[HandlerField.CalTotal.value],
                })
                item['extra']['status'] = celery_task.result[
                    HandlerField.Status.value]
        result.append(item)
    return JsonResponse(response_json({
        'count': Tasks.objects.count(),
        'results': result
    }))
