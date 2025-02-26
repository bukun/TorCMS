from pathlib import Path

from django.core.management.base import BaseCommand



class Command(BaseCommand):
    help = '清空数据库迁移文件'

    def handle(self, *args, **options):
        for wdir in Path('.').rglob('migrations'):
            if wdir.is_dir():
                pass
            else:
                continue

            for wfile in wdir.glob('00*.py'):
                print(wfile)
                wfile.unlink()
