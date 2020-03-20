from enum import Enum, unique
import math
import re
import time

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

@unique
class HandlerErrcode(Enum):
    """
    处理器返回的错误代码
    """
    Success = 0 # 成功
    NotCrawled = 1 # 视频未被全部抓取
    NotHandled = 2 # 视频标签未被全部处理
    NotCalculated = 3 # 视频平均数据未被全部计算

@unique
class RecordStatus(Enum):
    """
    当日视频记录的处理状态
    """
    Crawled = 0 # 全部视频被抓取
    Handled = 1 # 全部视频已处理标签关系
    Calculated = 2 # 全部视频已计算每日的平均数据

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
    return int(time.mktime(time.strptime(date, "%Y%m%d")))

def timestamp_to_date(timestamp):
    """
    时间戳转为yyyyMMdd日期
    """
    return int(time.strftime("%Y%m%d", time.localtime(timestamp)))

def timestamp_round_to_day(timestamp):
    """
    时间戳取整到天
    """
    return timestamp - ((timestamp + 28800) % 86400)

def str_to_clear(str):
    """
    去除字符串中的标点符号，并将大写字母变为小写
    """
    return re.sub(r"[^a-zA-Z0-9\u4e00-\u9fa5]", "", str).lower()