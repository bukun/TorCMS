import random

from django.contrib.auth.hashers import make_password
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

from faker import Faker

def create_superuser(username, email, password):
    if User.objects.filter(username=username).exists():
        print('Superuser already exists')
        User.objects.filter(username=username).update(
            email=email,
            # 简单使用
            password=make_password(password),
            vip_kind=1,
        )
    else:
        User.objects.create_superuser(username=username, email=email, password=password)
        print('Superuser created successfully')

class Command(BaseCommand):
    help = '初始化实际使用的数据库'


    def handle(self, *args, **options):
        passwd = Faker().password()
        create_superuser('admin', Faker().email(), passwd)

        print('username: admin')
        print('passwd: {}'.format(passwd))

        print('QED')
