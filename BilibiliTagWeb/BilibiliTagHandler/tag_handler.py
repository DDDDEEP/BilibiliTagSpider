"""
Bilibili视频标签处理器

- 从原视频数据中提取视频标签，存入tags表。
- 整理[分区-日期-标签]对应的视频列表，存入video_tag表
"""

import math
import time

import numpy
from pymongo import MongoClient

from helpers import HandlerErrcode, RecordStatus, STAT_NAME, print_time, str_to_clear, timestamp_round_to_day, date_to_timestamp


class TagHandler:
    """
    Bilibili视频标签处理器
    """
    def __init__(self, host, database, user, password):
        # 实例变量. 给对象赋值
        self._client = MongoClient(host=host,
                                   port=27017,
                                   username=user,
                                   password=password,
                                   authSource='admin')
        self._db = self._client[database]
        self.handle_cur = 0
        self.handle_total = 0
        self.calculate_cur = 0
        self.calculate_total = 0

    def reset_data(self):
        self.handle_cur = 0
        self.handle_total = 0
        self.calculate_cur = 0
        self.calculate_total = 0

    def start(self, type_id, time_from, time_to):
        """
        开始处理
        """
        time_from = date_to_timestamp(time_from)
        time_to_end = date_to_timestamp(time_to) + 24 * 3600

        time_start = time.time()
        self.reset_data()

        # 处理对应视频的标签关系
        errcode_handle = self.start_handle(type_id, time_from, time_to_end)
        if errcode_handle != HandlerErrcode.Success:
            return errcode_handle.value

        # 计算每日视频的数据均值
        errcode_calculate = self.start_calculate(type_id, time_from,
                                                 time_to_end)
        if errcode_calculate != HandlerErrcode.Success:
            return errcode_calculate.value

        print_time('总时间：', time.time() - time_start)
        return HandlerErrcode.Success.value

    def start_handle(self, type_id, time_from, time_to_end):
        """
        处理对应视频的标签关系
        """
        if not self.judge_record(type_id, time_from, time_to_end,
                                 RecordStatus.Crawled.value):
            print('对应时间范围内的视频未全部抓取，不进行处理')
            return HandlerErrcode.NotCrawled

        time_start = time.time()
        videos = self._db['videos'].find({
            'tid': type_id,
            'pubdate': {
                '$gte': time_from,
                '$lt': time_to_end
            }
        }).sort([('tid', 1), ('pubdate', 1)]).batch_size(500)
        self.handle_cur = 0
        self.handle_total = videos.count()
        print("将要处理{count}个视频的标签关系".format(count=self.handle_total))

        lower_time = time_from
        higher_time = time_from + 86400
        for video in videos:
            for tag in video['tags'].split(','):
                tag = str_to_clear(tag)
                self.save_tags(tag)
                self.save_videotag(video['aid'], type_id,
                                   timestamp_round_to_day(video['pubdate']),
                                   tag)

            if video['pubdate'] >= higher_time:
                # 判断并记录当日视频是否全部处理完成
                self.save_record(type_id, lower_time,
                                 RecordStatus.Handled.value)
                lower_time += 86400
                higher_time += 86400

            self.handle_cur += 1
            if self.handle_cur % 500 == 0:
                print_time(
                    "处理{count}个视频的标签关系所用时间：".format(count=self.handle_cur),
                    time.time() - time_start)

        # 记录最后一日的视频全部完成
        self.save_record(type_id, lower_time, RecordStatus.Handled.value)
        print_time("处理{count}个视频的标签关系所用时间：".format(count=self.handle_cur),
                   time.time() - time_start)

        return HandlerErrcode.Success

    def start_calculate(self, type_id, time_from, time_to_end):
        """
        计算单日视频的均值并记录
        """
        if not self.judge_record(type_id, time_from, time_to_end,
                                 RecordStatus.Handled.value):
            print('对应时间范围内的标签关系未被全部处理，不进行计算')
            return HandlerErrcode.NotHandled

        time_start = time.time()
        video_tags = self._db['video_tag'].find({
            'tid': type_id,
            'pubdate': {
                '$gte': time_from,
                '$lt': time_to_end
            }
        }).sort([('tid', 1), ('pubdate', 1)]).batch_size(500)
        self.calculate_cur = 0
        self.calculate_total = video_tags.count()
        print("将要计算{count}个标签关系的均值数据".format(count=self.calculate_total))

        lower_time = time_from
        higher_time = time_from + 86400
        for video_tag in video_tags:
            stats = {}
            # 计算对应记录的数据均值
            for stat_code, stat_name in STAT_NAME.items():
                stats[stat_name] = []
            for aid in video_tag['aids']:
                video = self._db['videos'].find_one({'aid': aid})
                for stat_code, stat_name in STAT_NAME.items():
                    stats[stat_name].append(video[stat_name])

            # 更新对应记录的数据均值
            update_json = {}
            for stat_code, stat_name in STAT_NAME.items():
                update_json['avg_' + stat_name] = math.ceil(
                    numpy.mean(stats[stat_name]))
            self._db['video_tag'].update_one({'_id': video_tag['_id']},
                                             {'$set': update_json})

            if video_tag['pubdate'] >= higher_time:
                # 判断并记录当日视频是否全部处理完成
                self.save_record(type_id, lower_time,
                                 RecordStatus.Calculated.value)
                lower_time += 86400
                higher_time += 86400

            self.calculate_cur += 1
            if self.calculate_cur % 500 == 0:
                print_time(
                    "计算{count}个标签关系所用时间：".format(count=self.calculate_cur),
                    time.time() - time_start)

        # 记录最后一日的视频全部完成
        self.save_record(type_id, lower_time, RecordStatus.Calculated.value)
        print_time("计算{count}个标签关系所用时间：".format(count=self.calculate_cur),
                   time.time() - time_start)

        return HandlerErrcode.Success

    def judge_record(self, type_id, time_from, time_to_end, status):
        """
        判断时间范围内的视频是否大于等于指定的状态值
        """
        days = (time_to_end - time_from) // 86400
        count = self._db['records'].count_documents({
            'tid': type_id,
            'pubdate': {
                '$gte': time_from,
                '$lt': time_to_end
            },
            'status': {
                '$gte': status
            }
        })
        return days == count

    def save_record(self, tid, pubdate, status):
        """
        更新对应爬取记录的状态值
        """
        self._db['records'].update_one({
            'tid': tid,
            'pubdate': pubdate,
        }, {'$set': {
            'status': status,
        }})

    def save_tags(self, tag):
        """
        将标签存入tags表中
        """
        self._db['tags'].update_one({'name': tag},
                                    {'$setOnInsert': {
                                        'name': tag
                                    }},
                                    upsert=True)

    def save_videotag(self, aid, tid, pubdate, tag):
        """
        将视频号存入[分区-日期-标签]对应的视频列表
        """
        document_tag = self._db['tags'].find_one({'name': tag})
        self._db['video_tag'].update_one(
            {
                'tid': tid,
                'pubdate': pubdate,
                'tag_id': document_tag['_id']
            }, {
                '$addToSet': {
                    'aids': aid
                },
                '$setOnInsert': {
                    'avg_stat_view': 0,
                    'avg_stat_danmaku': 0,
                    'avg_stat_reply': 0,
                    'avg_stat_favorite': 0,
                    'avg_stat_coin': 0,
                    'avg_stat_share': 0,
                    'avg_stat_like': 0,
                    'avg_stat_dislike': 0,
                }
            },
            upsert=True)

    def get_tag_count_rank(self, type_id, time_from, time_to_end, count):
        """
        获取一段时间内，各标签的出现次数对应的排行
        """
        result = self._db['video_tag'].aggregate([
            {
                '$match': {
                    'tid': type_id,
                    'pubdate': {
                        '$gte': time_from,
                        '$lt': time_to_end
                    }
                }
            },
            {
                '$sort': {
                    'tid': 1,
                    'pubdate': 1,
                    'tag': 1
                }
            },
            {
                '$addFields': {
                    'count': {
                        '$size': '$aids'
                    }
                }
            },
            {
                '$group': {
                    '_id': '$tag_id',
                    'sum_count': {
                        '$sum': '$count'
                    }
                }
            },
            {
                '$sort': {
                    'sum_count': -1
                }
            },
            {
                '$limit': count
            },
            {
                '$lookup': {
                    'from': 'tags',
                    'localField': '_id',
                    'foreignField': '_id',
                    'as': 'tag'
                }
            },
            {
                '$unwind': {
                    'path': '$tag',
                }
            },
            {
                '$project': {
                    '_id': 0,
                    'tag_name': '$tag.name',
                    'sum_count': 1
                }
            },
        ], allowDiskUse=True)
        return list(result)

    def get_tag_avg_stat_rank(self, type_id, time_from, time_to_end, count,
                              stat_code, min_tag_count):
        """
        获取一段时间内，各标签对应的平均数据量的排行

        stat_code    -- 想要查询的数据量的代号，对应STAT_NAME
        min_tag_count -- 排行榜内的标签最少包含的视频数
        """
        stat_name = STAT_NAME[str(stat_code)]
        result = self._db['video_tag'].aggregate([
            {
                '$match': {
                    'tid': type_id,
                    'pubdate': {
                        '$gte': time_from,
                        '$lt': time_to_end
                    }
                }
            },
            {
                '$sort': {
                    'tid': 1,
                    'pubdate': 1,
                    'tag': 1
                }
            },
            {
                '$addFields': {
                    'count': {
                        '$size': '$aids'
                    },
                    stat_name: {
                        '$multiply': [{
                            '$size': '$aids'
                        }, '$avg_' + stat_name]
                    },
                }
            },
            {
                '$group': {
                    '_id': '$tag_id',
                    'sum_count': {
                        '$sum': '$count'
                    },
                    'total_' + stat_name: {
                        '$sum': '$' + stat_name
                    }
                }
            },
            {
                '$addFields': {
                    'avg_' + stat_name: {
                        '$divide': ['$total_' + stat_name, '$sum_count']
                    }
                }
            },
            {
                '$match': {
                    'sum_count': {
                        '$gte': min_tag_count
                    }
                }
            },
            {
                '$sort': {
                    'avg_' + stat_name: -1
                }
            },
            {
                '$limit': count
            },
            {
                '$lookup': {
                    'from': 'tags',
                    'localField': '_id',
                    'foreignField': '_id',
                    'as': 'tag'
                }
            },
            {
                '$unwind': {
                    'path': '$tag'
                }
            },
            {
                '$project': {
                    '_id': 0,
                    'tag_name': '$tag.name',
                    'sum_count': 1,
                    'avg_stat': {
                        '$trunc': ['$avg_' + stat_name, 2]
                    }
                }
            },
        ], allowDiskUse=True)
        return list(result)

    def create_test_rank_video(self):
        """
        创建测试排序接口的视频数据

        创建分区号17、投稿日期是2000-01-01的100个视频
        第一个视频标签为“标签0”,第2个视频标签为“标签0,标签1”，如此类推
        第一个视频的播放量是0，第一个视频的播放量是1，如此类推
        """
        timestamp = 946656000
        tags = ''
        for i in range(31):
            if i == 0:
                tags = f'标签{i}'
            else:
                tags += f',标签{i}'

            self._db['videos'].update_one({
                'aid': i,
            }, {
                '$setOnInsert': {
                    'created_at': int(time.time()),
                    'tid': 17,
                    'pubdate': timestamp,
                    'aid': i,
                    'tags': tags,
                },
                '$set': {
                    'updated_at': int(time.time()),
                    'title': f'测试视频{i}',
                    'duration': i,
                    'stat_view': i,
                    'stat_danmaku': i,
                    'stat_reply': i,
                    'stat_favorite': i,
                    'stat_coin': i,
                    'stat_share': i,
                    'stat_like': i,
                    'stat_dislike': i,
                }
            },
                                          upsert=True)

            self._db['records'].update_one({
                'tid': 17,
                'pubdate': timestamp,
            }, {'$set': {
                'status': RecordStatus.Crawled.value,
            }},
                                           upsert=True)
            timestamp += 86400
