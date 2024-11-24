from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import CrawlSource
from .resources import CrawlSourceResource
from django.db.models.aggregates import Count


class CrawlSourceAdmin(ImportExportModelAdmin):
    resource_class = CrawlSourceResource
    # 控制哪些字段会显示在Admin 的修改列表页面中
    list_display = ("title", "url", )


    list_per_page = 20

    # def get_count(self, obj):
    #     rec = CrawlSource.objects.annotate(num_posts=Count('crawl_document_en')).filter(title=obj.title)
    #
    #     return rec[0].num_posts
    #
    # get_count.short_description = '文档数量'
    # get_count.admin_order_field = 'get_count'


# 注册app的admin
admin.site.register(CrawlSource, CrawlSourceAdmin)
