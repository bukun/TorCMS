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
    list_display = ('username', 'email', 'mobile','jupyter_url',  'jupyter_port','get_groups')

    # 将源码的UserAdmin.fieldsets转换成列表格式
    # fieldsets = list(UserAdmin.fieldsets)
    fieldsets = (
        (None, {'fields': ['username', 'password', ]}),
        (_('通用信息'), {'fields': ('avatar_img', 'mobile', 'location', 'detailed_address',)}),
        (_('Jupyter用户信息'), {'fields': ('jupyter_url', 'jupyter_port')}),

        (_('权限'), {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        (_('重要日期'), {'fields': ('last_login', 'date_joined',)})
    )

    list_per_page = 20

    add_fieldsets = (
        (None, {u'fields': ('username', 'password1', 'password2')}),
        # 增加页面显示字段设置
        (_('通用信息'), {'fields': ('avatar_img', 'mobile',  'location', 'detailed_address',)}),


        (_('Jupyter用户信息'), {'fields': ('jupyter_url', 'jupyter_port')}),

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


    def get_readonly_fields(self, request, obj=None):
        if obj:  # obj为None时表示添加，非None时表示编辑
            return ['jupyter_port']
        else:
            return ['jupyter_port']



admin.site.register(myuser, myuseradmin)
admin.site.site_header = 'Resource Management Center'  # 设置header
# admin.site.site_title = '科学数据管理与可视化后台管理'
admin.site.site_title = 'Resource Management Center'
admin.site.unregister(Group)


class groupadmin(MPTTModelAdmin, ImportExportModelAdmin, admin.ModelAdmin):
    search_fields = ('id', 'name', 'type')
    list_display = ('name', 'type', 'parent',)

    filter_horizontal = ('permissions',)

    def formfield_for_manytomany(self, db_field, request=None, **kwargs):
        if db_field.name == 'permissions':
            qs = kwargs.get('queryset', db_field.remote_field.model.objects)
            # Avoid a major performance hit resolving permission names which
            # triggers a content_type load:
            kwargs['queryset'] = qs.select_related('content_type')
        return super().formfield_for_manytomany(db_field, request=request, **kwargs)


admin.site.register(admingroup, groupadmin)
