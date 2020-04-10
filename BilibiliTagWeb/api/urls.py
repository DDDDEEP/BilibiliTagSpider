import api.views as views
import api.rank.views as rank_views
import api.task.views as task_views
from django.urls import path

urlpatterns = [
    path('video', views.VideoViewSet.as_view({'get': 'list'}), name='video'),
    path('record', views.RecordViewSet.as_view({'get': 'list'}), name='record'),
    path('rank/tag_count',
         rank_views.get_tag_count_rank,
         name='rank.tag_count'),
    path('rank/tag_avg_stat',
         rank_views.get_tag_avg_stat_rank,
         name='rank.tag_avg_stat'),
    path('task/start_handler',
         task_views.start_handler,
         name="task.start_handler"),
    path('task/handler_progress',
         task_views.get_handler_progress,
         name="task.handler_progress"),
    path('task/start_spider',
         task_views.start_spider,
         name="task.start_spider"),
    path('task/spider_progress',
         task_views.get_spider_progress,
         name="task.spider_progress"),
    path('task/task_list',
         task_views.get_task_list,
         name="task.get_task_list"),
]
