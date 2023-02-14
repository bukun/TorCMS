# -*- coding:utf-8 -*-

import json
import re

import yaml
import random
import os
from torcms.core.tools import logger
from torcms.core import privilege
from torcms.handlers.post_handler import PostHandler
from torcms_metadata.handlers.meta_handler import MetadataHandler
from torcms.model.label_model import MPost2Label
from torcms.model.post2catalog_model import MPost2Catalog
from torcms.model.category_model import MCategory
from torcms.core.tool.sqlite_helper import MAcces
from torcms.model.usage_model import MUsage
from torcms.model.post_model import MPost


class MetaExtHander(MetadataHandler):
    def get(self, *args, **kwargs):
        url_str = args[0]
        url_arr = self.parse_url(url_str)
        # if url_arr:
        #     self._redirect(url_arr)

        if url_str in ['data','index','']:
            self.index()
        elif url_arr[0] == '_cat_add':
            self._to_add(catid=url_arr[1])
        elif url_arr[0] == 'download_excel':

            self.download_xlsx(url_arr[1])
        elif url_arr[0] == '_add':
            if len(url_arr) == 2:
                self._to_add(uid=url_arr[1])
            else:
                self._to_add()
        elif len(url_arr) == 1 and len(url_str) >= 4:
            self._view_or_add(url_str)
        elif len(url_arr) == 2:
            dict_get = {
                '_edit_kind': self._to_edit_kind,
                '_edit': self._to_edit,
                '_delete': self._delete,
                '_downxml': self._downxml,
            }
            dict_get.get(url_arr[0])(url_arr[1])
        else:
            self.show404()

    def ext_post_data(self, **kwargs):
        data_dic = kwargs['postdata']
        ext_dict = {}
        if 'gcat0' in data_dic and data_dic['gcat0'].startswith('27'):
            ext_dict['ext_yaml'] = data_dic['extra_yaml']
            ext_dict['def_json'] = json.dumps(yaml.load(ext_dict['ext_yaml']))
        else:
            pass
        return ext_dict

    @privilege.auth_view
    def viewinfo(self, postinfo):
        '''
        查看 Post.
        '''

        __ext_catid = postinfo.extinfo.get('def_cat_uid', '')
        cat_enum1 = MCategory.get_qian2(__ext_catid[:2]) if __ext_catid else []
        rand_recs, rel_recs = self.fetch_additional_posts(postinfo.uid)

        self._chuli_cookie_relation(postinfo.uid)

        catinfo = None
        p_catinfo = None

        post2catinfo = MPost2Catalog.get_first_category(postinfo.uid)
        if post2catinfo:
            catinfo = MCategory.get_by_uid(post2catinfo.tag_id)
            if catinfo:
                p_catinfo = MCategory.get_by_uid(catinfo.pid)

        kwd = self._the_view_kwd(postinfo)

        MPost.update_misc(postinfo.uid, count=True)
        MAcces.add(postinfo.uid)

        ############################################################################
        if postinfo.extinfo.get('def_cat_pid') == '2200':
            if postinfo.extinfo.get('ext_map_layers'):
                import subprocess
                run_str = '/usr/bin/python3 lhy_datamap_xml_script.py {}'.format(postinfo.extinfo.get('ext_map_layers','q_cp_imagery_imagery'))
                ret = subprocess.Popen(run_str, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, encoding="utf-8")
                run_out, run_err = ret.communicate()

                MPost.update_jsonb(postinfo.uid, extinfo={'ext_xml': str(run_out)})

        ############################################################################

        if self.get_current_user() and self.userinfo:
            MUsage.add_or_update(self.userinfo.uid, postinfo.uid,
                                 postinfo.kind)

        self.set_cookie('user_pass', kwd['cookie_str'])

        tmpl = self.ext_tmpl_view(postinfo)

        if self.userinfo:
            recent_apps = MUsage.query_recent(self.userinfo.uid, postinfo.kind,
                                              6).objects()[1:]
        else:
            recent_apps = []
        logger.info('The Info Template: {0}'.format(tmpl))

        self.render(
            tmpl,
            kwd=dict(kwd, **self.ext_view_kwd(postinfo)),
            postinfo=postinfo,
            userinfo=self.userinfo,
            catinfo=catinfo,
            pcatinfo=p_catinfo,
            relations=rel_recs,
            rand_recs=rand_recs,
            subcats=MCategory.query_sub_cat(p_catinfo.uid) if p_catinfo else '',
            ad_switch=random.randint(1, 18),
            tag_info=filter(lambda x: not x.tag_name.startswith('_'),
                            MPost2Label.get_by_uid(postinfo.uid).objects()),
            recent_apps=recent_apps,
            cat_enum=cat_enum1)

    def _downxml(self, uid):

        save_file = './static/upload/xml/'
        out_docx = os.path.join(save_file, 'xx_' + str(uid) + '.xml')
        if not os.path.exists(save_file):
            os.makedirs(save_file)
        if os.path.exists(out_docx):
            try:
                os.remove(out_docx)
            except Exception:
                pass

        with open(out_docx, "w") as xml_f:
            result = MPost.get_by_uid(uid)
            xml_f.write(result.extinfo.get('ext_xml', ''))
            xml_f.close()

        if out_docx:
            output = {'down_code': 1, 'down_url': str(out_docx)[1:]}

        else:
            output = {'down_code': 0}

        return json.dump(output, self)
