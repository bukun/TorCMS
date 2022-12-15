# -*- coding:utf-8 -*-

'''
根据ID检索json信息：分类，标签等
'''
import json
import tornado.gen
import tornado.web
from torcms.core.base_handler import BaseHandler
from torcms.model.category_model import MCategory
from torcms.model.post_model import MPost
from torcms.model.label_model import MPost2Label
from torcms.model.relation_model import MCorrelation
from torcms.core.tools import logger
from torcms_taginfo.taglib import taginfo

class DatalistHandler(BaseHandler):
    def initialize(self, **kwargs):
        super(DatalistHandler, self).initialize()
        self.kind = '3'
        self.filter_view = True

    def get(self, *args, **kwargs):
        url_str = args[0]
        url_arr = self.parse_url(url_str)

        if url_str == '' or url_str == 'list':
            self.list()
        elif url_arr[0] == '_add':
            self._to_add()
        elif len(url_arr) == 1:

            self.findid(url_arr[0])

        else:
            kwd = {
                'info': 'The Page not Found.',
            }
            self.show404(kwd=kwd)

    def post(self, *args, **kwargs):

        url_str = args[0]
        logger.info('Post url: {0}'.format(url_str))
        url_arr = self.parse_url(url_str)

        if url_arr[0] in ['_add']:
            self.add()
        elif url_arr[0] in ['j_get_tag']:
            self.get_tag()
        else:
            post_data = self.get_request_arguments()

            keyword = post_data['keyword']

            self.redirect('/dataset/{0}'.format(keyword))

    def set_default_headers(self):
        # print（"setting headers!!!"）
        self.set_header("Access-Control-Allow-Origin", "*")  # 这个地方可以写域名
        self.set_header("Access-Control-Allow-Headers", "x-requested-with")
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')

    def index(self):
        self.render('../torcms_taginfo/search_data.html',
                    userinfo=self.userinfo,
                    kwd={})

    def list(self):
        dataset_json = []
        recs = MPost.query_all(kind='3', limit='100000')
        for info in recs:
            if 'cpbh' in info.extinfo:
                pass
            else:
                continue

            rec = MPost.get_by_uid(info.uid)
            dic_data = {
                "ID": rec.uid,
                "product_number": rec.extinfo['cpbh'],

            }
            dataset_json.append(dic_data)

        return json.dump(dataset_json, self, ensure_ascii=False)


    def _to_add(self, **kwargs):
        '''
        Used for info1.
        '''

        self.render('../torcms_taginfo/post_add.html',
                    tag_infos=MCategory.query_all(by_order=True,
                                                  kind=self.kind),
                    userinfo=self.userinfo,

                    kwd={'uid': ''})

    def fetch_post_data(self):
        '''
        fetch post accessed data. post_data, and ext_dic.
        '''
        post_data = {}
        for key in self.request.arguments:
            post_data[key] = self.get_arguments(key)[0]

        return post_data

    def get_tag(self):
        print('=' * 40)
        post_data = json.loads(self.request.body)
        print(post_data)
        for key in post_data:
            print(key)
        tag_arr = taginfo.get_tag_by_title(post_data)
        dic_data = {
            "Title": post_data['title'],
            "Category": '',
            "Label": tag_arr,
        }
        return json.dump(dic_data, self, ensure_ascii=False)

    @tornado.gen.coroutine
    def add(self, **kwargs):
        '''
        in infor.
        '''

        post_data = self.fetch_post_data()

        title = post_data['title'].strip()

        if len(title) < 2:
            kwd = {
                'info': 'Title cannot be less than 2 characters',
                'link': '/'
            }
            self.render('misc/html/404.html', userinfo=self.userinfo, kwd=kwd)

        # if 'gcat0' in post_data:
        #     pass
        # else:
        #     return False

        tag_arr = taginfo.get_tag_by_title(post_data)
        dic_data = {
            "title": post_data['title'],
            "Category ID": '',
            "Label": tag_arr,
        }

        return json.dump(dic_data, self, ensure_ascii=False)



    def findid(self, uid):
        recs = MPost.query_by_extinfo(key='cpbh', val=uid)
        for rec in recs:
            print(rec.uid, rec.title)
        if recs.count() == 0:
            rec = None
            rec2 = None

        for xrec in recs:
            if xrec.kind == '3':
                rec = xrec
            if xrec.kind == '9':
                rec2 = xrec

        if rec:

            cat_info = MCategory.get_by_uid(rec.extinfo['gcat0'])
            sdg_cat_list=[]
            for ii in range(0, 5):

                try:
                    cat_info2 = MCategory.get_by_uid(rec2.extinfo['gcat' + str(ii)])
                    sdg_cat_list.append({"category_sdg_id":cat_info2.uid, "category_sdg_name":cat_info2.name})
                except:
                    pass
            label = self.get_label(rec.uid)
            relate_info = self.get_relateinfo(rec.uid)
            dic_data = {
                # "ID": rec.uid,
                "product_number": rec.extinfo['cpbh'],
                'title': rec.title,
                "category_subject_id": cat_info.uid,
                "category_subject_name": cat_info.name,
                "category_sdg": sdg_cat_list,
                # "category_sdg_name": sdg_cat_list,
                # "relevant_information": relate_info,
                "tags": label,
            }

        else:
            dic_data = {
                "error": "产品编号有误，请 <a href='/dataset/'>重新输入<a>"
            }

        return json.dump(dic_data, self, ensure_ascii=False)

    def get_label(self, rec_id):
        label_list = []
        lab_info = MPost2Label.get_by_uid(rec_id).objects()
        for label in lab_info:
            label_list.append(label.tag_name)
        return label_list

    def get_relateinfo(self, rec_id):
        rel_list = []
        relate_infos = MCorrelation.get_app_relations(rec_id)
        if relate_infos:
            for rel_info in relate_infos:
                pro_id = MPost.get_by_uid(rel_info.rel_id)
                rel_list.append({'ID': rel_info.rel_id, 'product_number': pro_id.extinfo['cpbh']})
            return rel_list
        else:
            return ''
