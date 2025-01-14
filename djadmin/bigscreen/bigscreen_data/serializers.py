import json
from .models import BigScreenData
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from bigscreen.jump_btn.models import JumpBtn
from django.core import serializers as django_serializers
from qgis.qgis_map.models import qgismap,BigScreenMapCategory


class BigScreenSerializer(serializers.ModelSerializer):
    qgis_map = serializers.SerializerMethodField()
    fast_location_btn = serializers.SerializerMethodField()

    def get_qgis_map(self, obj):
        data_rec = []
        for map_category in obj.qgis_map.all():
            rec = qgismap.objects.filter(bigscreencategory=map_category.id).all()
            data = django_serializers.serialize('json', rec)
            json_data = json.loads(data)

            # 保存分类名
            json_data[0]['name']=map_category.name

            # 获取标签名
            all_label_name=[]
            for label in json_data[0]['fields']['label']:
                rec = BigScreenMapCategory.objects.filter(id=label).all()
                data = django_serializers.serialize('json', rec)

                label_json_data = json.loads(data)

                all_label_name.append(label_json_data[0]['fields']['name'])
            json_data[0]['fields']['label']=all_label_name

            data_rec.append(json_data[0])

        return data_rec

    def get_fast_location_btn(self, obj):
        data_rec = []
        for btn_rec in obj.fast_location_btn.all():
            rec = JumpBtn.objects.filter(id=btn_rec.id).filter()
            data = django_serializers.serialize('json', rec)
            json_data = json.loads(data)
            data_rec.append(json_data[0])

        return data_rec
        # return data_rec[0]



    class Meta:
        model = BigScreenData
        fields = '__all__'


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super(MyTokenObtainPairSerializer, cls).get_token(user)

        # 添加额外信息
        token['username'] = user.username
        return token
