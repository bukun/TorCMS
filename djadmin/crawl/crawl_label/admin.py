from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from ..crawl_source.models import CrawlLabel
from .resources import LabelResource
from django.db.models.aggregates import Count


class CrawlLabelAdmin(ImportExportModelAdmin):
    resource_class = LabelResource
    # 控制哪些字段会显示在Admin 的修改列表页面中
    list_display = ("name", "get_count")
    list_filter = ("is_en",)

    list_per_page = 20

    def get_count(self, obj):
        if obj.is_en == 1:
            rec = CrawlLabel.objects.annotate(num_posts=Count('crawl_document_en')).filter(name=obj.name)
        else:
            rec = CrawlLabel.objects.annotate(num_posts=Count('crawl_document')).filter(name=obj.name)
        return rec[0].num_posts

    get_count.short_description = '数据数量'
    get_count.admin_order_field = 'count'


# 注册app的admin
admin.site.register(CrawlLabel, CrawlLabelAdmin)
