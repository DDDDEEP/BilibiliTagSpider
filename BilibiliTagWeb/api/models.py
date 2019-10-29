# Create your models here.
from djongo import models
from django import forms
# import mongoengine


# class VideoStat(models.Model):
#     view = models.IntegerField()
#     danmaku = models.IntegerField()
#     reply = models.IntegerField()
#     favorite = models.IntegerField()
#     coin = models.IntegerField()
#     share = models.IntegerField()
#     like = models.IntegerField()
#     dislike = models.IntegerField()

#     class Meta:
#         abstract = True

class Videos(models.Model):
    _id = models.ObjectIdField(primary_key=True)
    aid = models.IntegerField()
    tid = models.IntegerField()
    title = models.CharField(max_length=128)
    duration = models.IntegerField()
    pubdate = models.IntegerField()
    tags = models.CharField(max_length=128)
    updated_at = models.IntegerField()

    stat_view = models.IntegerField()
    stat_danmaku = models.IntegerField()
    stat_reply = models.IntegerField()
    stat_favorite = models.IntegerField()
    stat_coin = models.IntegerField()
    stat_share = models.IntegerField()
    stat_like = models.IntegerField()
    stat_dislike = models.IntegerField()
    
    objects = models.DjongoManager()

    class Meta:
        db_table = 'videos'
        indexes = [
            models.Index(fields=['tid', 'pubdate', ]),
            models.Index(fields=['aid', ]),
            models.Index(fields=['_id', ]),
        ]
