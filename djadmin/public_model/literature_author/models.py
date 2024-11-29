import markdown
from django.db import models
from django.contrib.auth import get_user_model
from base.models import basemodel
from mdeditor.fields import MDTextField
from django.contrib.sites.models import Site
from django.utils.safestring import mark_safe
from public_model.public_country.models import PublicCountry
User = get_user_model()

gender_CHOICES = [
('0', '---------'),
('1', 'Male'),
('2', 'Female'),
]
class LiteratureAuthor(basemodel):
    name=models.CharField(blank=True,unique=True, null=False, max_length=255, verbose_name="姓名")
    gender=models.CharField(choices=gender_CHOICES, verbose_name="性别",default='0')
    nation = models.ForeignKey(PublicCountry, on_delete=models.CASCADE, blank=True, null=True,
                                related_name='literature_author', verbose_name='国家')
    department=models.CharField(blank=True, null=True, max_length=255, verbose_name="部门")
    business=models.CharField(blank=True, null=True, max_length=255, verbose_name="职务")
    profession=models.CharField(blank=True, null=True, max_length=255, verbose_name="专业")
    email=models.CharField(blank=True, null=True, max_length=255, verbose_name="邮箱")
    tel=models.CharField(blank=True, null=True, max_length=255, verbose_name="电话")
    cnt_md = MDTextField(verbose_name="简介", null=True, blank=True)
    logo = models.ImageField(upload_to='author/imgs/', max_length=255, null=True, blank=True,
                             verbose_name="图片")
    sites = models.ManyToManyField(Site,blank=True, related_name='literature_author', verbose_name='Site')

    def __str__(self):
        return self.name
    def get_html_content(self):
        html_content = markdown.markdown(self.cnt_md)
        return mark_safe(html_content)

    class Meta(basemodel.Meta):
        db_table = 'literature_authors'
        verbose_name = "Literature Author"
        verbose_name_plural = verbose_name
