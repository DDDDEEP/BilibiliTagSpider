"""
Bilibili视频标签处理器

- 从原视频数据中提取视频标签，存入tags表。
- 整理[分区-日期-标签]对应的视频列表，存入video_tag表
"""

from bson.code import Code
import math
import numpy
import time

from helpers import *
from pymongo import DESCENDING, MongoClient

class TagHandler:
    """
    Bilibili视频标签处理器
    """
    def __init__(self, host, database, user, password):
        # 实例变量. 给对象赋值
        self.client = MongoClient(
            host = host,
            port = 27017, 
            username = user,
            password = password,
            authSource = "admin"
        )
        self.db = self.client[database]

    def start(self, type_id, time_from, time_to_end):
        """
        开始处理
        """
        time_start = time.time()
        
        # 处理对应视频的标签关系
        errcode_handle = self.start_handle(type_id, time_from, time_to_end)
        if errcode_handle != HandlerErrcode.Success:
            return errcode_handle

        # 计算每日视频的数据均值
        errcode_calculate = self.start_calculate(type_id, time_from, time_to_end)
        if errcode_handle != HandlerErrcode.Success:
            return errcode_handle
        
        print_time("总时间：", time.time() - time_start) 
        return HandlerErrcode.Success
    
    def start_handle(self, type_id, time_from, time_to_end):
        """
        处理对应视频的标签关系
        """
        if not self.judge_record(type_id, time_from, time_to_end, RecordStatus.Crawled.value):
            print("对应时间范围内的视频未全部抓取，不进行处理")
            return HandlerErrcode.NotCrawled

        time_start = time.time()
        videos = self.db["videos"].find(
                {
                    "tid": type_id,
                    "pubdate": {
                        "$gte": time_from,
                        "$lt": time_to_end
                    }
                }
            ).sort([
                ("tid", 1),
                ("pubdate", 1)
            ]).batch_size(500)
        print("将要处理{count}个视频的标签关系".format(count=videos.count()))   

        count = 0
        lower_time = time_from
        higher_time = time_from + 86400
        for video in videos:
            for tag in video["tags"].split(","):
                tag = str_to_clear(tag)
                self.save_tags(tag)
                self.save_videotag(
                    video["aid"],
                    type_id,
                    timestamp_round_to_day(video["pubdate"]),
                    tag
                )
            
            if video["pubdate"] >= higher_time:
                # 判断并记录当日视频是否全部处理完成
                self.save_record(type_id, lower_time, RecordStatus.Handled.value)
                lower_time += 86400
                higher_time += 86400
                
            count += 1
            if count % 500 == 0:
                print_time("处理{count}个视频的标签关系所用时间：".format(count=count), time.time() - time_start)

        # 记录最后一日的视频全部完成
        self.save_record(type_id, lower_time, RecordStatus.Handled.value)
        print_time("处理{count}个视频的标签关系所用时间：".format(count=count), time.time() - time_start)

        return HandlerErrcode.Success

    def start_calculate(self, type_id, time_from, time_to_end):
        """
        计算单日视频的均值并记录
        """
        if not self.judge_record(type_id, time_from, time_to_end, RecordStatus.Handled.value):
            print("对应时间范围内的标签关系未被全部处理，不进行计算")
            return HandlerErrcode.NotHandled

        time_start = time.time()
        video_tags = self.db["video_tag"].find(
                {
                    "tid": type_id,
                    "pubdate": {
                        "$gte": time_from,
                        "$lt": time_to_end
                    }
                }
            ).sort([
                ("tid", 1),
                ("pubdate", 1)
            ]).batch_size(500)
        print("将要计算{count}个标签关系的均值数据".format(count=video_tags.count()))

        count = 0
        lower_time = time_from
        higher_time = time_from + 86400
        for video_tag in video_tags:
            stats = {}
            # 计算对应记录的数据均值
            for name in STAT_NAMES:
                stats[name] = []
            for aid in video_tag["aids"]:
                video = self.db["videos"].find_one({"aid": aid})
                for name in STAT_NAMES:
                    stats[name].append(video[name])

            # 更新对应记录的数据均值
            update_json = {}
            for name in STAT_NAMES:
                update_json["avg_" + name] = math.ceil(numpy.mean(stats[name]))
            self.db["video_tag"].update_one(
                {
                    "_id": video_tag["_id"]
                },
                {
                    "$set": update_json
                }
            )

            if video_tag["pubdate"] >= higher_time:
                # 判断并记录当日视频是否全部处理完成
                self.save_record(type_id, lower_time, RecordStatus.Calculated.value)
                lower_time += 86400
                higher_time += 86400
            
            count += 1
            if count % 500 == 0:
                print_time("计算{count}个标签关系所用时间：".format(count=count), time.time() - time_start)

        # 记录最后一日的视频全部完成
        self.save_record(type_id, lower_time, RecordStatus.Calculated.value)
        print_time("计算{count}个标签关系所用时间：".format(count=count), time.time() - time_start)

        return HandlerErrcode.Success

    def judge_record(self, type_id, time_from, time_to_end, status):
        """
        判断时间范围内的视频是否大于等于指定的状态值
        """
        days = (time_to_end - time_from) // 86400
        count = self.db["records"].count_documents({
            "tid": type_id,
            "pubdate": {
                "$gte": time_from,
                "$lt": time_to_end
            },
            "status": {
                "$gte": status
            }
        })
        return days == count

    def save_record(self, tid, pubdate, status):
        """
        更新对应爬取记录的状态值
        """
        self.db["records"].update_one(
            {
                "tid": tid,
                "pubdate": pubdate,
            },
            {
                "$set": {
                    "status": status,
                }
            }
        )

    def save_tags(self, tag):
        """
        将标签存入tags表中
        """
        self.db["tags"].update_one(
            {
                "name": tag
            },
            {
                "$setOnInsert": {
                    "name": tag
                }
            },
            upsert=True
        )

    def save_videotag(self, aid, tid, pubdate, tag):
        """
        将视频号存入[分区-日期-标签]对应的视频列表
        """
        document_tag = self.db["tags"].find_one({"name":tag})
        self.db["video_tag"].update_one(
            { 
                "tid": tid,
                "pubdate": pubdate,
                "tag_id": document_tag["_id"]
            },
            {
                "$addToSet": {
                    "aids": aid
                }
            },
            upsert=True
        )

    def get_tag_count_rank(self, type_id, time_from, time_to_end, count):
        """
        获取一段时间内，各标签的出现次数对应的排行
        """
        # 进行MapReduce
        tag_count_rank = self.db["video_tag"].map_reduce(
                Code(
                    """
                    function(){
                        emit(this.tag_id, this.aids.length);
                    }
                    """
                ),
                Code(
                    """
                    function(key,values){  
                        return eval(values.join("+"));
                    }
                    """
                ),
                {
                    "inline": 1
                },
                query = {
                    "tid": type_id,
                    "pubdate": {
                        "$gte": time_from,
                        "$lt": time_to_end
                    }
                },
                sort = {
                    "tid": 1,
                    "pubdate": 1,
                    "tag": 1
                }
            ).find().sort("value", DESCENDING).limit(count)

        # 格式化结果
        result = []
        for record in tag_count_rank:
            result.append({
                "tag": self.db["tags"].find_one({"_id": record["_id"]})["name"],
                "count": int(record["value"])
            })
        return result

    def get_tag_avg_stat_rank(self, type_id, time_from, time_to_end, count, stat_index, min_tag_count):
        """
        获取一段时间内，各标签对应的平均数据量的排行

        stat_index    -- 想要查询的数据量的索引代号，对应STAT_NAMES
        min_tag_count -- 排行榜内的标签最少包含的视频数
        """
        # 进行MapReduce
        tag_avg_stat_rank = self.db["video_tag"].map_reduce(
                Code(
                    """
                    function(){
                        emit(this.tag_id, this.aids.length);
                    }
                    """
                ),
                Code(
                    """
                    function(key,values){  
                        return eval(values.join("+"));
                    }
                    """
                ),
                {
                    "inline": 1
                },
                query = {
                    "tid": type_id,
                    "pubdate": {
                        "$gte": time_from,
                        "$lt": time_to_end
                    }
                },
                sort = {
                    "tid": 1,
                    "pubdate": 1,
                    "tag": 1
                }
            ).find().sort("value", DESCENDING).limit(count)

        # 格式化结果
        result = []
        for record in tag_count_rank:
            result.append({
                "tag": self.db["tags"].find_one({"_id": record["_id"]})["name"],
                "count": int(record["value"])
            })
        return result

    