from django.apps import AppConfig
import os
default_app_config = 'user.IndexConfig'
# 获取当前app的命名
def get_current_app_name(_file):
    return os.path.split(os.path.dirname(_file))[-1]
# 重写类IndexConfig
class IndexConfig(AppConfig):
    name = get_current_app_name(__file__)
    verbose_name = '用户信息数据表'