import json
from .models import ChangChunProject
from rest_framework import serializers
from django.core import serializers as django_serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_gis.serializers import GeometrySerializerMethodField
from django.contrib.gis.geos import Polygon


class PolygonSerializerField(serializers.Field):
    def to_representation(self, value: Polygon):
        # 将Polygon对象序列化为JSON兼容的格式

        data = django_serializers.serialize("geojson", ChangChunProject.objects.filter(location=value),
                                            geometry_field="location", fields=["cadastre_id"])
        return json.loads(data)



    def to_internal_value(self, data):
        # 将JSON数据反序列化为Polygon对象
        coords = data.get('coordinates')
        srid = data.get('srid')
        return Polygon(coords, srid=srid)


class GeofeaSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    geometry = GeometrySerializerMethodField()
    location = PolygonSerializerField()

    def get_geometry(self, obj):
        return obj.location

    class Meta:
        model = ChangChunProject
        fields = '__all__'
        geo_field = ['geometry']


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super(MyTokenObtainPairSerializer, cls).get_token(user)

        # 添加额外信息
        token['username'] = user.username
        return token
