from django.db import models
from django.contrib.auth import get_user_model
from base.models import basemodel, basecategory

User = get_user_model()


class igaiscategory(basemodel, basecategory):
    class Meta(basemodel.Meta):
        db_table = 'igaiscategory'
        verbose_name = "IGAIS分类"
        verbose_name_plural = verbose_name
