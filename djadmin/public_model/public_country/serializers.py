from public_model.literature_author.models import PublicCountry
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class AuthorSerializer(serializers.ModelSerializer):

    class Meta:
        model = PublicCountry
        fields = '__all__'


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super(MyTokenObtainPairSerializer, cls).get_token(user)

        # 添加额外信息
        token['username'] = user.username
        return token
