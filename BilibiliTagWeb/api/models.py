# Create your models here.
from djongo import models


class Videos(models.Model):
    _id = models.ObjectIdField(primary_key=True)
    tid = models.IntegerField()
    pubdate = models.IntegerField()
    aid = models.IntegerField()
    tags = models.CharField(max_length=128)

    title = models.CharField(max_length=128)
    duration = models.IntegerField()
    stat_view = models.IntegerField()
    stat_danmaku = models.IntegerField()
    stat_reply = models.IntegerField()
    stat_favorite = models.IntegerField()
    stat_coin = models.IntegerField()
    stat_share = models.IntegerField()
    stat_like = models.IntegerField()
    stat_dislike = models.IntegerField()

    created_at = models.IntegerField()
    updated_at = models.IntegerField()

    objects = models.DjongoManager()

    class Meta:
        db_table = 'videos'
        indexes = [
            models.Index(fields=[
                'tid',
                'pubdate',
            ]),
            models.Index(fields=[
                '_id',
            ]),
        ]
        constraints = [
            models.UniqueConstraint(fields=[
                'aid',
            ], name='unique_aid'),
        ]


class Tags(models.Model):
    _id = models.ObjectIdField(primary_key=True)
    name = models.CharField(max_length=64)

    objects = models.DjongoManager()

    class Meta:
        db_table = 'tags'
        indexes = [
            models.Index(fields=[
                '_id',
            ]),
        ]
        constraints = [
            models.UniqueConstraint(fields=[
                'name',
            ], name='unique_name'),
        ]


class AidCollection(models.Model):
    aid = models.IntegerField()

    class Meta:
        abstract = True


class VideoTag(models.Model):
    _id = models.ObjectIdField(primary_key=True)
    tid = models.IntegerField()
    pubdate = models.IntegerField()
    tag_id = models.BinaryField(max_length=12)
    aids = models.ArrayField(model_container=AidCollection)

    avg_stat_view = models.IntegerField()
    avg_stat_danmaku = models.IntegerField()
    avg_stat_reply = models.IntegerField()
    avg_stat_favorite = models.IntegerField()
    avg_stat_coin = models.IntegerField()
    avg_stat_share = models.IntegerField()
    avg_stat_like = models.IntegerField()
    avg_stat_dislike = models.IntegerField()

    class Meta:
        db_table = 'video_tag'
        indexes = [
            models.Index(fields=[
                '_id',
            ]),
        ]
        constraints = [
            models.UniqueConstraint(fields=[
                'tid',
                'pubdate',
                'tag_id',
            ],
                                    name='unique_tid_pubdate_tagid')
        ]


class Records(models.Model):
    # 记录每日对应爬虫记录的状态
    _id = models.ObjectIdField(primary_key=True)
    tid = models.IntegerField()
    pubdate = models.IntegerField()
    status = models.IntegerField()  # 该日爬虫记录的状态，0为已爬取完成，1为已处理完成

    objects = models.DjongoManager()

    class Meta:
        db_table = 'records'
        indexes = [
            models.Index(fields=[
                '_id',
            ]),
        ]
        constraints = [
            models.UniqueConstraint(fields=['tid', 'pubdate'],
                                    name='unique_tid_pubdate'),
        ]


class Tasks(models.Model):
    # 记录异步任务的信息
    _id = models.ObjectIdField(primary_key=True)
    task_id = models.CharField(max_length=36)
    task_type = models.IntegerField()  # 0为爬虫，1为处理器
    tid = models.IntegerField()
    time_from = models.IntegerField()
    time_to = models.IntegerField()
    time_start = models.IntegerField()  # 任务创建时间
    time_end = models.IntegerField()  # 任务结束时间，默认为-1

    objects = models.DjongoManager()

    class Meta:
        db_table = 'tasks'
        indexes = [
            models.Index(fields=[
                '_id',
            ]),
            models.Index(fields=[
                'time_start',
            ]),
        ]
        constraints = [
            models.UniqueConstraint(fields=['task_id'],
                                    name='unique_task_id'),
        ]