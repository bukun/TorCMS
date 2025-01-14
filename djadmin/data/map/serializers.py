from data.categorys.models import map
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from data.dataset.serializers import DataSerializer

class MapSerializer(serializers.ModelSerializer):
    data = DataSerializer()

    class Meta:
        model = map
        fields = '__all__'


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super(MyTokenObtainPairSerializer, cls).get_token(user)

        # 添加额外信息
        token['username'] = user.username
        return token
