from django.db import models

from modelcluster.fields import ParentalKey

from wagtail.models import Page, Orderable
from wagtail.fields import RichTextField
from wagtail.admin.panels import FieldPanel, MultiFieldPanel, InlinePanel
from wagtail.search import index


class BlogPage(Page):
    # 页面有 title（标题，Page 类自带）、body（内容）、date（日期）、feed_image（头图）三个
    # feed_image 是外部键，是 wagtailimages.Image 类
    body = RichTextField()
    date = models.DateField("Post date")
    feed_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    # 可以通过 body 搜索，通过 date 筛选
    search_fields = Page.search_fields + [
        index.SearchField('body'),
        index.FilterField('date'),
    ]

    # 在 cms 管理后台中，当新建 1 个 BlogPage 时，会出现 date、body、related_links（相关链接） 字段
    # 其中 related_links 是 wagtail 中实现 many-to-many 关系的方式，下边会提到
    content_panels = Page.content_panels + [
        FieldPanel('date'),
        FieldPanel('body'),
        InlinePanel('related_links', heading="Related links", label="Related link"),
    ]
    # 在 cms 管理后台中，当新建 1 个 BlogPage 时，高级选项里会出现常见 common page configuration、feed_image 选项
    promote_panels = [
        MultiFieldPanel(Page.promote_panels, "Common page configuration"),
        FieldPanel('feed_image'),
    ]

    # 在哪些类型的页面下可以创建 BlogPage 作为子页面、BlogPage 下可以创建哪些子页面，空就是无限制
    parent_page_types = []
    subpage_types = []


# 定义了 related_link（相关链接）的类
class BlogPageRelatedLink(Orderable):
    # 和 BlogPage 相关联的字段
    page = ParentalKey(BlogPage, on_delete=models.CASCADE, related_name='related_links')

    # 链接名称和 url
    name = models.CharField(max_length=255)
    url = models.URLField()

    # 当在 cms admin 里添加相关链接时，有哪些字段
    panels = [
        FieldPanel('name'),
        FieldPanel('url'),
    ]
