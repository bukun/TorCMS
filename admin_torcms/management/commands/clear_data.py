import importlib
import inspect
from pathlib import Path

from django.core.management.base import BaseCommand

import admin_torcms.models as uu
from admin_torcms.models import *


class Command(BaseCommand):
    help = '清空数据库迁移文件'

    def handle(self, *args, **options):
        for rec in TabPost.objects.filter().all():
            print(rec.uid)
        TabPost.objects.all().delete()
        for rec in TabPost.objects.filter().all():
            print(rec.uid)

        print(inspect.getmodule(uu).__name__)
        print(inspect.getmodule(uu).__dict__)
        for key in inspect.getmodule(uu).__dict__:
            print(key)
            if key.startswith('Tab'):
                pass
            else:
                continue

            vv = getattr(uu, key)
            # vv = importlib.import_module(f'admin_torcms.models.{key }')

            print(vv)
            vv.objects.all().delete()
