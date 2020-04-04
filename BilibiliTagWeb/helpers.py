from enum import IntEnum, unique, Enum
import math
import re
import time
from threading import Thread

# stat数据字段代号
STAT_NAME = {
    '0': 'stat_view',
    '1': 'stat_danmaku',
    '2': 'stat_reply',
    '3': 'stat_favorite',
    '4': 'stat_coin',
    '5': 'stat_share',
    '6': 'stat_like',
    '7': 'stat_dislike',
}


@unique
class ScrapyField(Enum):
    """
    爬虫字段常量
    """
    VideoCur = 'video_item_cur'  # 当前爬取的视频数
    VideoTotal = 'video_item_total'  # 需爬取的视频总数


@unique
class HandlerField(Enum):
    """
    处理器字段常量
    """
    Status = 'status'  # 返回值
    HandleCur = 'handle_cur'  # 当前处理的数量
    HandleTotal = 'handle_total'  # 需处理的总数
    CalCur = 'calculate_cur'  # 当前计算的数量
    CalTotal = 'calculate_total'  # 需计算的总数


@unique
class HandlerErrcode(IntEnum):
    """
    处理器返回的错误代码
    """
    Success = 0  # 成功
    Running = 1  # 正常运行中
    AlreadyRunning = 2  # 处理器已经在运行
    NotCrawled = 3  # 视频未被全部抓取
    NotHandled = 4  # 视频标签未被全部处理
    NotCalculated = 5  # 视频平均数据未被全部计算


@unique
class TaskType(IntEnum):
    """
    异步任务类型
    """
    Scrapy = 0  # 爬虫
    Handler = 1  # 处理器


@unique
class RecordStatus(IntEnum):
    """
    当日视频记录的处理状态
    """
    Crawled = 0  # 全部视频被抓取
    Handled = 1  # 全部视频已处理标签关系
    Calculated = 2  # 全部视频已计算每日的平均数据


class ThreadWithReturnValue(Thread):
    """
    返回执行结果的线程
    """
    def __init__(self,
                 group=None,
                 target=None,
                 name=None,
                 args=(),
                 kwargs=None,
                 *,
                 daemon=None):
        super(ThreadWithReturnValue, self).__init__(group=group,
                                                    target=target,
                                                    name=name,
                                                    args=args,
                                                    kwargs=kwargs)
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
    print("{}{}时{}分{}秒".format(description, hours, minutes, seconds))


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