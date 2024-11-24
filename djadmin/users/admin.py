from django.contrib import admin
from .models import myuser, admingroup, roletype
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import Group
from .resources import UsersResource
from import_export.admin import ImportExportModelAdmin
from mptt.admin import MPTTModelAdmin


# 先注册
class myuseradmin(ImportExportModelAdmin, UserAdmin):
    resource_class = UsersResource
    list_display = ('username', 'get_group_type', 'email', 'mobile', 'get_groups')

    # 将源码的UserAdmin.fieldsets转换成列表格式
    # fieldsets = list(UserAdmin.fieldsets)
    fieldsets = (
        (None, {'fields': ['username', 'password', ]}),
        (_('通用信息'), {'fields': ('avatar_img', 'mobile', 'state', 'location', 'detailed_address',)}),

        # (_('所属组织和经营主体'), {'fields': ('belong_jyztzz',)}),
        # # (_('所属组织和经营主体'), {'fields': ('belong_jyztzz', 'belong_department')}),
        # (_('专家角色信息'), {'fields': ('field', 'professional_title')}),
        # (_('政府角色信息'), {'fields': ('government_department', 'government_duties')}),

        (_('权限'), {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        (_('重要日期'), {'fields': ('last_login', 'date_joined',)})
    )

    list_per_page = 20

    add_fieldsets = (
        (None, {u'fields': ('username', 'password1', 'password2')}),
        # 增加页面显示字段设置
        (_('通用信息'), {'fields': ('avatar_img', 'mobile', 'state', 'location', 'detailed_address',)}),

        # (_('所属组织和经营主体'), {'fields': ('belong_jyztzz',)}),
        # (_('专家角色信息'), {'fields': ('field', )}),
        # (_('政府角色信息'), {'fields': ('government_department', 'government_duties','professional_title')}),

        (_('权限'), {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        (_('重要日期'), {'fields': ('last_login', 'date_joined')})
    )

    # list_editable = ('mobile', 'email')
    def get_groups(self, obj):
        rec = myuser.objects.get(username__exact=obj.username)
        groups = []
        for group in rec.groups.all():
            groups.append(group.name)
        return str(groups)

    get_groups.short_description = '用户角色'
    get_groups.admin_order_field = 'get_groups'

    def get_name(self, obj):
        return str(obj.last_name) + (obj.first_name)

    get_name.short_description = '姓名'
    get_name.admin_order_field = 'get_name'

    def get_group_type(self, obj):
        rec = myuser.objects.get(username__exact=obj.username)
        groups_type = []
        for group in rec.groups.all():
            g_rec = admingroup.objects.get(name__exact=group.name)
            gtype = g_rec.get_type_display()
            groups_type.append(gtype)
        return groups_type

    get_group_type.short_description = '角色类型'
    get_group_type.admin_order_field = 'get_group_type'


admin.site.register(myuser, myuseradmin)
admin.site.site_header = '科学数据管理与可视化后台管理'  # 设置header
admin.site.site_title = '科学数据管理与可视化后台管理'
admin.site.unregister(Group)


class groupadmin(MPTTModelAdmin,ImportExportModelAdmin, admin.ModelAdmin):
    search_fields = ('id', 'name', 'type')
    list_display = ( 'name', 'type', 'parent',)

    filter_horizontal = ('permissions',)

    # todo  编辑的时候要不要显示他所有的用户？然后显示了主要是能不能修改？
    # todo  得有个只是点击查看每个项的内容的按键
    # todo 反向查找 但是 懵了
    # https://blog.csdn.net/weixin_62935305/article/details/125509506
    # def get_all_group_users(self, obj):
    #     # group = AdminGroup.objects.select_related('background_user_belong_department').get(name__exact=obj.name)
    #     group = AdminGroup.objects.get(id=obj.id)
    #     print('-----obj.id--------')
    #     print(obj.id)
    #     print('-----group--------')
    #     print(group)
    #     print('-----group.background_user_belong_department--------')
    #     print(group.background_user_belong_department)
    #     all_group_user_list = group.background_user_belong_department.all()
    #     # print('-----all_group_user_list--------')
    #     # print(all_group_user_list)
    #     print('-----len all_group_user_list--------')
    #     print(len(all_group_user_list))
    #     return_list = []
    #     for one_user in all_group_user_list:
    #         print('-----one_user--------')
    #         print(one_user)
    #
    #     # groups_type = []
    #     # for group in rec.groups.all():
    #     #     print('------group-------')
    #     #     print(group)
    #     #     g_rec = AdminGroup.objects.get(name__exact=group.name)
    #     #     gtype = g_rec.get_type_display()
    #     #     groups_type.append(gtype)
    #     return all_group_user_list

    # get_all_group_users.short_description = '角色所有用户'
    # get_all_group_users.admin_order_field = 'get_all_group_users'

    def formfield_for_manytomany(self, db_field, request=None, **kwargs):
        if db_field.name == 'permissions':
            qs = kwargs.get('queryset', db_field.remote_field.model.objects)
            # Avoid a major performance hit resolving permission names which
            # triggers a content_type load:
            kwargs['queryset'] = qs.select_related('content_type')
        return super().formfield_for_manytomany(db_field, request=request, **kwargs)

admin.site.register(admingroup, groupadmin)