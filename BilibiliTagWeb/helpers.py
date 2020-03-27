from enum import IntEnum, unique
import math
import re
import time
from threading import Thread

# stat数据字段名，为方便处理，使用索引值作为代号
STAT_NAMES = [
    'stat_view',
    'stat_danmaku',
    'stat_reply',
    'stat_favorite',
    'stat_coin',
    'stat_share',
    'stat_like',
    'stat_dislike'
]

# spider.stats对应字段
SCRAPY_STAT_VIDEO_CUR = 'video_item_cur'
SCRAPY_STAT_VIDEO_TOTAL = 'video_item_total'

@unique
class HandlerErrcode(IntEnum):
    """
    处理器返回的错误代码
    """
    Success        = 0 # 成功
    Running        = 1 # 正常运行中
    AlreadyRunning = 2 # 处理器已经在运行
    NotCrawled     = 3 # 视频未被全部抓取
    NotHandled     = 4 # 视频标签未被全部处理
    NotCalculated  = 5 # 视频平均数据未被全部计算

@unique
class RecordStatus(IntEnum):
    """
    当日视频记录的处理状态
    """
    Crawled = 0 # 全部视频被抓取
    Handled = 1 # 全部视频已处理标签关系
    Calculated = 2 # 全部视频已计算每日的平均数据

@unique
class SpiderStat(IntEnum):
    """
    当日视频记录的处理状态
    """
    Crawled = 0 # 全部视频被抓取
    Handled = 1 # 全部视频已处理标签关系
    Calculated = 2 # 全部视频已计算每日的平均数据

class ThreadWithReturnValue(Thread):
    """
    返回执行结果的线程
    """
    def __init__(self, group=None, target=None, name=None,
                 args=(), kwargs=None, *, daemon=None):
        super(ThreadWithReturnValue, self).__init__(group=group, target=target, name=name,
                                                    args=args, kwargs=kwargs)
        self._return = None

    def run(self):
        if self._target is not None:
            self._return = self._target(*self._args, **self._kwargs)
            
    def join(self, *args):
        super(ThreadWithReturnValue, self).join(self, *args)
        return self._return
    
    def get_return(self):
        return self._return

def stat_to_int(val):
    """
    Bilibili视频数据转为int（部分数据项可能返回"--"）
    """
    return int(val if val != '--' else 0)
    
def print_time(description, total_seconds):
    """
    打印格式化后的秒数
    """
    total_seconds = math.ceil(total_seconds)
    hours = total_seconds // 3600
    minutes = total_seconds % 3600 // 60
    seconds = total_seconds % 3600 % 60
    print("{}{}时{}分{}秒".format(description,hours,minutes,seconds))

def date_to_timestamp(date):
    """
    yyyyMMdd日期转为时间戳
    """
    date = str(date)
    return int(time.mktime(time.strptime(str(date), '%Y%m%d')))

def timestamp_to_date(timestamp):
    """
    时间戳转为yyyyMMdd日期
    """
    return int(time.strftime('%Y%m%d', time.localtime(timestamp)))

def timestamp_round_to_day(timestamp):
    """
    时间戳取整到天
    """
    return timestamp - ((timestamp + 28800) % 86400)

def str_to_clear(str):
    """
    去除字符串中的标点符号，并将大写字母变为小写
    """
    return re.sub(r"[^a-zA-Z0-9\u4e00-\u9fa5]", '', str).lower()