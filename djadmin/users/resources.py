from import_export import resources
from import_export.fields import Field
from import_export.widgets import ForeignKeyWidget

from .models import myuser
from django.contrib.auth import get_user_model

User = get_user_model()


class UsersResource(resources.ModelResource):
    class Meta:
        model = myuser
        import_id_fields = ['name']

        # # 导入前检查是否存在用户，不存在这创建用户，如果存在则将用户关联到模型
        # def before_import(self, dataset, using_transactions, dry_run, **kwargs):
        #     for work_num in dataset['username']:
        #         username = str(work_num)
        #         password = "dxd@" + str(123456)
        #         if not User.objects.filter(username=username).exists():
        #             User.objects.create_user(username=work_num, password=password, is_staff=True, is_superuser=False)
