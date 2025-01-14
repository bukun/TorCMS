import json
from place.geofea.models  import PlanarFeatures
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.core import serializers as django_serializers
from django.contrib.gis.geos import Polygon


class PolygonSerializerField(serializers.Field):
    def to_representation(self, value: Polygon):
        # 将Polygon对象序列化为JSON兼容的格式

        data = django_serializers.serialize("geojson", PlanarFeatures.objects.filter(location=value),
                                            geometry_field="location", fields=["location_name"])
        return json.loads(data)

    #

    def to_internal_value(self, data):
        # 将JSON数据反序列化为Polygon对象
        coords = data.get('coordinates')
        srid = data.get('srid')
        return Polygon(coords, srid=srid)


class ApiAppSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    location = PolygonSerializerField()

    class Meta:
        model = PlanarFeatures
        fields = '__all__'


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super(MyTokenObtainPairSerializer, cls).get_token(user)

        # 添加额外信息
        token['username'] = user.username
        return token
