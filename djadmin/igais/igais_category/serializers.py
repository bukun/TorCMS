from .models import igaiscategory
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class IgaisCategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = igaiscategory
        fields = '__all__'


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super(MyTokenObtainPairSerializer, cls).get_token(user)

        # 添加额外信息
        token['username'] = user.username
        return token
