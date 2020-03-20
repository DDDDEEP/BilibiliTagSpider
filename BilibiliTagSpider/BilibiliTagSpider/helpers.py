import time

def stat_to_int(val):
    """
    Bilibili视频数据转为int（部分数据项可能返回"--"）
    """
    return int(val if val != "--" else 0)

def date_to_timestamp(date):
    """
    yyyyMMdd日期转为时间戳
    """
    date = str(date)
    return int(time.mktime(time.strptime(date, "%Y%m%d")))

def timestamp_to_date(timestamp):
    """
    时间戳转为yyyyMMdd日期
    """
    return int(time.strftime("%Y%m%d", time.localtime(timestamp)))