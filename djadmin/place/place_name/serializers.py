import json
from .models import PlaceName
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from django.core import serializers as django_serializers
from django.contrib.gis.geos import Point


class PolygonSerializerField(serializers.Field):
    def to_representation(self, value: Point):
        # 将Point对象序列化为JSON兼容的格式

        return {'coordinates': value.coords, 'srid': value.srid}


class ApiAppSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    location = PolygonSerializerField()

    class Meta:
        model = PlaceName
        fields = '__all__'


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super(MyTokenObtainPairSerializer, cls).get_token(user)

        # 添加额外信息
        token['username'] = user.username
        return token
