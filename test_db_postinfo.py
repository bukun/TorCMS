# 针对导入的测试内容进行测试，当前测试页面时候能正常打开。
# 测试添加的能容能否正确打开。
from tornado.testing import AsyncHTTPSTestCase
from server import APP
from torcms.model.post_model import MPost
from torcms.model.category_model import MCategory

post_infos = MPost.query_all(kind='1')
info_infos = MPost.query_all(kind='3')
# tutorial_infos = MPost.query_all(kind='k')
tags = MCategory.query_all()
# labels = MCategory.query_all(kind='z')


class TestPostHandler(AsyncHTTPSTestCase):
    def get_app(self):
        return APP

    def test_post(self):
        for post in post_infos:
            response = self.fetch('/post/{0}'.format(post.uid))
            self.assertEqual(response.code, 200)
        for info in info_infos:
            response = self.fetch('/info/{0}'.format(info.uid))
            self.assertEqual(response.code, 200)
        # Todo:教程访问方式与分类不同，导入的内容需要重新考虑。
        # for tutorial in tutorial_infos:
        #     response = self.fetch('/tutorial/{0}'.format(tutorial.uid))
        #     self.assertEqual(response.code, 200)

    def test_tags(self):
        for tag in tags:
            if tag.kind == '1' or tag.kind == 'k' or tag.kind == 'm':
                response = self.fetch('/list/{0}'.format(tag.slug))
                self.assertEqual(response.code, 200)
            elif tag.kind == '3':
                print('tag.uid')
                print(tag.uid)
                response = self.fetch('/filter/{0}'.format(tag.uid))
                self.assertEqual(response.code, 200)

    # Todo:标签打开方式暂未确定,需要判断标签与那个分类链接.
    # def test_label(self):
    #     for label in labels:
    #         response = self.fetch('/label/{0}/{1}'.format(label.kind,label.slug))
    #         self.assertEqual(response.code, 200)
