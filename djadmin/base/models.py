import datetime

from django.db import models
import uuid
from mptt.models import MPTTModel, TreeForeignKey
from django.contrib.sites.models import Site
import markdown
from django.utils.safestring import mark_safe
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
current_site = Site.objects.get_current()


def get_template():
    if current_site.id == 1:
        parent_template = 'yaou_base.html'
    elif current_site.id in [2, 3]:
        parent_template = 'zhongmeng_base.html'
    elif current_site.domain == "http://127.0.0.1:6792/":
        parent_template = 'yaou_base.html'
    else:
        parent_template = 'base.html'
    return parent_template


class basecategory(MPTTModel, models.Model):
    parent = TreeForeignKey('self', on_delete=models.DO_NOTHING, null=True, blank=True, related_name='children',
                            verbose_name='上级名称')
    name = models.CharField(blank=True, null=False, unique=True, max_length=255, verbose_name="分类名称")

    def __str__(self):
        if hasattr(self, 'name'):  # hasattr 是Python中是反射的一种用法
            return self.name
        else:
            return self.id

    class Meta:
        abstract = True
        ordering = ['id']


class basemodel(models.Model):
    # id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    # 公共字段部分： 创建时间、更新时间、描述
    # auto_now_add 第一次创建数据时自动添加当前时间
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    # auto_now 每次更新数据时自动添加当前时间
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    edit_count = models.IntegerField(default=0, verbose_name='修改次数', editable=False)
    order = models.IntegerField(blank=True, null=True, default=1, verbose_name="排序")

    def save(self, *args, **kwargs):
        # 在保存前，增加修改次数
        self.edit_count += 1

        # 保存对象
        super(basemodel, self).save(*args, **kwargs)

    def __str__(self):
        # 判断当前数据对象是否有name属性，如果有，返回name，如果没有，返回描述
        if hasattr(self, 'name'):  # hasattr 是Python中是反射的一种用法
            return self.name
        else:
            return self.id
    def get_html_content(self):
        content = ""
        for line in self.cnt_md.split("\n"):
            content += line.strip("  ") if "```" in line else line
            content += "\n"
        html_content = markdown.markdown(content, extensions=[
            'markdown.extensions.extra',  # 转化标题，字体等
            'markdown.extensions.codehilite',  # 高亮功能
            'markdown.extensions.toc',  # 将表单渲染为html， document类型
        ])

        return mark_safe(html_content)
    class Meta:
        abstract = True  # 定义抽象表，不会创建数据库表
        ordering = ['id']  # 根据id排序（默认为顺序排序）




# 状态
class statetype(models.IntegerChoices):
    type1 = 1, '启用'
    type2 = 0, '禁用'


# 权限查看
class permissionviewtype(models.IntegerChoices):
    type1 = 1, '全部可见'
    type2 = 0, '部分可见'
def get_paginator(data_recs, request):
    paginator = Paginator(data_recs, 20)  # 实例化一个分页对象, 每页显示10个
    page = request.GET.get('page')  # 从URL通过get页码，如?page=3
    try:
        page_obj = paginator.page(page)
    except PageNotAnInteger:
        page_obj = paginator.page(1)  # 如果传入page参数不是整数，默认第一页
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)
    is_paginated = True if paginator.num_pages > 1 else False  # 如果页数小于1不使用分页
    return is_paginated, page_obj

def get_html_content(self):
    content = ""
    for line in self.cnt_md.split("\n"):
        content += line.strip("  ") if "```" in line else line
        content += "\n"
    html_content = markdown.markdown(content, extensions=[
        'markdown.extensions.extra',  # 转化标题，字体等
        'markdown.extensions.codehilite',  # 高亮功能
        'markdown.extensions.toc',  # 将表单渲染为html， document类型
    ])

    return mark_safe(html_content)