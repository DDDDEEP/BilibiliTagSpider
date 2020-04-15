from bson import ObjectId
from bson.errors import InvalidId
from rest_framework import serializers
from django.utils.encoding import smart_text

from . import models


# 解决ObjectId的bug
class ObjectIdField(serializers.Field):
    """ Serializer field for Djongo ObjectID fields """
    def to_internal_value(self, data):
        # Serialized value -> Database value
        try:
            # Get the ID, then build an ObjectID instance using it
            return ObjectId(str(data))
        except InvalidId:
            raise serializers.ValidationError(
                '`{}` is not a valid ObjectID'.format(data))

    def to_representation(self, value):
        # Database value -> Serialized value
        # User submitted ID's might not be properly structured
        if not ObjectId.is_valid(value):
            raise InvalidId
        return smart_text(value)


class TagIdField(serializers.Field):
    def to_internal_value(self, data):
        # Serialized value -> Database value
        try:
            # Get the ID, then build an ObjectID instance using it
            return ObjectId(str(data))
        except InvalidId:
            raise serializers.ValidationError(
                '`{}` is not a valid ObjectID'.format(data))

    def to_representation(self, value):
        # Database value -> Serialized value
        # User submitted ID's might not be properly structured
        if not ObjectId.is_valid(value):
            raise InvalidId
        return models.Tags.objects.filter(_id=value).first().name


class VideoSerializer(serializers.ModelSerializer):
    _id = ObjectIdField(read_only=True)

    class Meta:
        model = models.Videos
        fields = '__all__'


class RecordSerializer(serializers.ModelSerializer):
    _id = ObjectIdField(read_only=True)

    class Meta:
        model = models.Records
        fields = '__all__'


class TagSerializer(serializers.ModelSerializer):
    _id = ObjectIdField(read_only=True)

    class Meta:
        model = models.Tags
        fields = '__all__'


class VideoTagSerializer(serializers.ModelSerializer):
    _id = ObjectIdField(read_only=True)
    tag_id = TagIdField(read_only=True)

    class Meta:
        model = models.VideoTag
        fields = '__all__'
