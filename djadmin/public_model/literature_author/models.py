import markdown
from django.db import models
from django.contrib.auth import get_user_model
from base.models import basemodel
from mdeditor.fields import MDTextField
from django.contrib.sites.models import Site
from django.utils.safestring import mark_safe

User = get_user_model()

gender_CHOICES = [
('0', '---------'),
('1', 'Male'),
('2', 'Female'),
]

class PublicCountry(basemodel):
    name=models.CharField(blank=True,unique=True, null=False, max_length=255, verbose_name="名称")


    sites = models.ManyToManyField(Site,blank=True, related_name='public_country', verbose_name='Site')

    def __str__(self):
        return self.name


    class Meta(basemodel.Meta):
        db_table = 'public_country'
        verbose_name = "国家管理"
        verbose_name_plural = verbose_name

class LiteratureAuthor(basemodel):
    name=models.CharField(blank=True,unique=True, null=False, max_length=255, verbose_name="姓名")
    gender=models.CharField(choices=gender_CHOICES, verbose_name="性别",default='0',max_length=255)
    nation = models.ForeignKey(PublicCountry, on_delete=models.CASCADE, blank=True, null=True,
                                related_name='literature_author', verbose_name='国家')
    department=models.CharField(blank=True, null=True, max_length=255, verbose_name="部门")
    business=models.CharField(blank=True, null=True, max_length=255, verbose_name="职务")
    profession=models.CharField(blank=True, null=True, max_length=255, verbose_name="专业")
    email=models.CharField(blank=True, null=True, max_length=255, verbose_name="邮箱")
    tel=models.CharField(blank=True, null=True, max_length=255, verbose_name="电话")
    cnt_md = MDTextField(verbose_name="简介", null=True, blank=True)
    logo = models.ImageField(upload_to='author/imgs/', max_length=255, null=True, blank=True, verbose_name="图片")
    sites = models.ManyToManyField(Site,blank=True, related_name='literature_author', verbose_name='Site')

    def __str__(self):
        return self.name


    class Meta(basemodel.Meta):
        db_table = 'literature_authors'
        verbose_name = "作者管理"
        verbose_name_plural = verbose_name



class LiteratureDate(basemodel):
    pub_date=models.CharField(blank=True,unique=True, null=False, max_length=255, verbose_name="日期")
    sites = models.ManyToManyField(Site,blank=True, related_name='literature_date', verbose_name='Site')

    def __str__(self):
        return self.pub_date

    class Meta(basemodel.Meta):
        db_table = 'literature_date'
        verbose_name = "日期管理"
        verbose_name_plural = verbose_name

