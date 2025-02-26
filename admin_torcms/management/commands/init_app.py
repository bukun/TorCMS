import random

from django.contrib.auth.hashers import make_password
from django.core.management.base import BaseCommand
from faker import Faker


class Command(BaseCommand):
    help = '初始化实际使用的数据库'

    def handle(self, *args, **options):
        # create_superuser('administor', 'adn@example.com', 'v1Wi7PSlXGjJcG')

        print('QED')
