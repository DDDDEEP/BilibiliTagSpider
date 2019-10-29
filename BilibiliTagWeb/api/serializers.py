from rest_framework import serializers
from . import models

# 解决ObjectId的bug
from bson import ObjectId
from bson.errors import InvalidId
from django.utils.encoding import smart_text


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


class VideoSerializer(serializers.ModelSerializer):
    _id = ObjectIdField(read_only=True)

    # stat = serializers.SerializerMethodField()

    class Meta:
        model = models.Videos
        fields = '__all__'
        
    # TODO: EmbeddedModelField对应的get方法r，已遗弃
    # def get_stat(self, obj):
    #     return_data = None
    #     if type(obj.stat) == list:
    #         embedded_list = []
    #         for item in obj.stat:
    #             embedded_dict = item.__dict__
    #             for key in list(embedded_dict.keys()):
    #                 if key.startswith('_'):
    #                     embedded_dict.pop(key)
    #             embedded_list.append(embedded_dict)
    #         return_data = embedded_list
    #     else:
    #         embedded_dict = obj.stat.__dict__
    #         for key in list(embedded_dict.keys()):
    #             if key.startswith('_'):
    #                 embedded_dict.pop(key)
    #         return_data = embedded_dict
    #     return return_data

    # def to_representation(self, instance):
    #     ret = super(VideoSerializer, self).to_representation(instance)
    #     # check the request is list view or detail view
    #     is_list_view = isinstance(self.instance, list)
    #     extra_ret = {'key': 'list value'} if is_list_view else {
    #         'key': 'single value'}
    #     ret.update(extra_ret)
    #     return ret
