from data.categorys.models import labels
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class LabelsSerializer(serializers.ModelSerializer):

    class Meta:
        model = labels
        fields = '__all__'


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super(MyTokenObtainPairSerializer, cls).get_token(user)

        # 添加额外信息
        token['username'] = user.username
        return token
