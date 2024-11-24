from .models import myuser, admingroup
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class UsersSerializer(serializers.ModelSerializer):
    # username = serializers.HiddenField(default=serializers.CurrentUserDefault())
    password = serializers.ReadOnlyField(source="myuser.password")
    # groups = serializers.HiddenField(default=serializers.CurrentUserDefault())
    user_groups = serializers.SerializerMethodField()
    user_permissions = serializers.StringRelatedField(many=True, read_only=True)
    user_role = serializers.SerializerMethodField()

    class Meta:
        model = myuser
        fields = '__all__'

    def get_user_groups(self, obj):
        rec = myuser.objects.get(username__exact=obj.username)
        groups_info = []
        for group in rec.groups.all():
            g_rec = admingroup.objects.get(name__exact=group.name)
            gtype = g_rec.get_type_display()

            groups_info.append(
                {"grout_id": g_rec.id, "grout_name": g_rec.name, "group_type": gtype, "group_parent": str(g_rec.parent),
                 "group_permissions": [g_per.name for g_per in g_rec.permissions.all()]})
        return groups_info

    #   todo  排列一下用户的角色 超级管理员就显示”超级管理员“，前台用户那就选择权限是前台用户的
    #         具体只显示哪个啥的以后再确定

    # todo 前端需要根据不同的角色来显示不同的模块
    def get_user_role(self, obj):
        rec = myuser.objects.get(username__exact=obj.username)

        # 超级管理员
        if obj.is_superuser:
            return '超级管理员'

        for group in rec.groups.all():
            g_rec = admingroup.objects.get(name__exact=group.name)
            gtype = g_rec.get_type_display()

            # 如果有‘前台用户管理’分类的角色，就返回第一个角色的名称
            if gtype == '前台用户管理':
                return g_rec.name
        # 啥角色没有就不显示角色
        return ''


class myuserregisterserializer(serializers.ModelSerializer):

    class Meta:
        model = myuser
        fields = '__all__'


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super(MyTokenObtainPairSerializer, cls).get_token(user)

        # 添加额外信息
        token['username'] = user.username
        return token
class GroupSerializer(serializers.ModelSerializer):
    parent = serializers.SerializerMethodField()

    class Meta:
        model = admingroup
        fields = ('id', 'name', 'type', 'parent')

    def get_parent(self, obj):
        if obj.parent is not None:
            return GroupSerializer(obj.parent).data
        else:
            return None