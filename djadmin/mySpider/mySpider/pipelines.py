# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.pipelines.images import ImagesPipeline
from scrapy.pipelines.files import FilesPipeline
from scrapy.exceptions import DropItem
import os
import scrapy

from urllib.parse import urlparse

from scrapy.utils.project import get_project_settings

settings = get_project_settings()
from crawl.crawl_document_en.models import CrawlDocumentEN
from crawl.crawl_label.models import CrawlLabel


class MyspiderPipeline:

    def process_item(self, item, spider):
        # print('ABC管道接收：{}' * 5)
        # 实例化Item对象

        if item.get('file'):
            item['file'] = 'scrapy/files/' + list(item['file'].values())[0]
        try:
            doc = CrawlDocumentEN.objects.get(title=item['title'])
            # Already exists, just update it
            instance = item.save(commit=False)
            instance.pk = doc.pk
        except CrawlDocumentEN.DoesNotExist:
            pass

        item.save()

        doc = CrawlDocumentEN.objects.get(title=item['title'])
        if item.get('label'):
            for tag_name in item['label']:
                tag, created = CrawlLabel.objects.get_or_create(name=tag_name)

                doc.label.add(tag)

        return item


class MyImagesPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        # image_urls 是一个数组
        for image_url in item['memo']:
            yield scrapy.Request(image_url)
        # # 如果image_urls是一个链接 也可以
        # if item.get('logo'):
        #     yield scrapy.Request(item['logo'])

    def item_completed(self, results, item, info):
        '''
        results:
        [(True, {
        'url': 'https://media.springernature.com/lw685/springer-static/image/art%3A10.1038%2Fs41467-023-43755-5/MediaObjects/41467_2023_43755_Fig1_HTML.png',
        'path': 'full/5d61273559ac9f628378130ee150792811057997.jpg',
        'checksum': 'd9aa687e95a1cdd1d1f3153c2ce17c71',
        'status': 'uptodate'})]
        '''

        image_paths = {x['url'].split('/')[-1]: x['path'] for ok, x in results if ok}

        if not image_paths:
            # 下载失败忽略该 Item 的后续处理
            # raise DropItem("Item contains no files")
            # item['memo'] = None
            pass
        else:
            # 将图片转移至以 post_id 为名的子目录中
            for (dest, src) in image_paths.items():
                dir = settings.get('IMAGES_STORE')
                newdir = dir + os.path.dirname(src) + '/'
                if not os.path.exists(newdir):
                    os.makedirs(newdir)
                os.rename(dir + src, newdir + dest)
            # 将保存路径保存于 item 中（image_paths 需要在 items.py 中定义）

            item['memo'] = image_paths

        return item

    # 重命名，若不重写这函数，图片名为哈希，就是一串乱七八糟的名字
    def file_path(self, request, response=None, info=None):

        file_name = request.url.split('/')[-1]
        return 'full/%s' % (file_name)


class PdfPipeline(FilesPipeline):
    def get_media_requests(self, item, info):
        if item.get('file'):
            yield scrapy.Request(item['file'])

    def item_completed(self, results, item, info):
        '''
        results:
        [(True, {
        'url': 'https://media.springernature.com/lw685/springer-static/image/art%3A10.1038%2Fs41467-023-43755-5/MediaObjects/41467_2023_43755_Fig1_HTML.png',
        'path': 'full/5d61273559ac9f628378130ee150792811057997.jpg',
        'checksum': 'd9aa687e95a1cdd1d1f3153c2ce17c71',
        'status': 'uptodate'})]
        '''

        file_paths = {x['url'].split('/')[-1]: x['path'] for ok, x in results if ok}

        if not file_paths:
            # 下载失败忽略该 Item 的后续处理
            # raise DropItem("Item contains no files")
            # item['memo'] = None
            pass
        else:
            # 将图片转移至以 post_id 为名的子目录中
            for (dest, src) in file_paths.items():
                dir = settings.get('FILES_STORE')
                newdir = dir + os.path.dirname(src) + '/'
                if not os.path.exists(newdir):
                    os.makedirs(newdir)
                os.rename(dir + src, newdir + dest)
            # 将保存路径保存于 item 中（image_paths 需要在 items.py 中定义）

            item['file'] = file_paths

        return item

    def file_path(self, request, response=None, info=None):
        file_name = request.url.split('/')[-1]
        return file_name
