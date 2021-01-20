'''
To run the script, run the following command the same direcotry.

    git clone https://github.com/bukun/pycsw_helper.git
'''
import os
import uuid

import html2text
from tornado.escape import xhtml_unescape

from pycsw_helper.csw_helper import MRecords
from torcms.model.post_model import MPost

mrec = MRecords()

h = html2text.HTML2Text()


def insert_into_db(postinfo):
    ab = h.handle(xhtml_unescape(postinfo.cnt_html))
    out_dic = {"identifier": 'uid-drr-{uid}'.format(uid=postinfo.uid),
               "typename": '',
               "schema": '',
               "mdsource": '',
               "insert_date": '',
               "xml": "",
               "anytext": ab,
               "language": '',
               "type": 'Zip File',
               "title": postinfo.title,
               "title_alternate": postinfo.title,
               "abstract": ab,
               "keywords": postinfo.keywords,
               "keywordstype": '',
               "parentidentifier": '',
               "relation": '',
               "time_begin": '',
               "time_end": '',
               "topicategory": '',
               "resourcelanguage": '',
               "creator": '',
               "publisher": '',
               "contributor": '',
               "organization": '',
               "securityconstraints": '',
               "accessconstraints": '',
               "otherconstraints": '',
               "date": postinfo.date,
               "date_revision": '',
               "date_creation": '',
               "date_publication": '',
               "date_modified": '',
               "format": '',
               "source": '',
               "crs": '',
               "geodescode": '',
               "denominator": '',
               "distancevalue": '',
               "distanceuom": '',
               "wkt_geometry": '',
               "servicetype": '',
               "servicetypeversion": '',
               "operation": '',
               "couplingtype": '',
               "operateson": '',
               "operatesonidentifier": '',
               "operatesoname": '',
               "degree": '',
               "classification": '',
               "conditionapplyingtoaccessanduse": '',
               "lineage": '',
               "responsiblepartyrole": '',
               "specificationtitle": '',
               "specificationdate": '',
               "specificationdatetype": '',
               # name,description,protocol,url[^„,[^„,]]”
               "links": "{name},{desc},{prot},url[{url1}]".format(
                   name='mm',
                   desc='ab',
                   prot='cc', url1='http://eng.wdc.cn/info/' + postinfo.uid
               )}

    print(out_dic['links'])

    # out_dic['conditionapplyingtoaccessanduse'] = raw_dic['USELIMIT'.lower()]
    out_dic["organization"] = 'OSGeo China Chapter'
    # out_dic["format"] = raw_dic['FORMDES'.lower()]
    # out_dic['date_publication'] = raw_dic['PUBTIME'.lower()]
    out_dic["source"] = 'http://www.maphub.cn'
    out_dic['publisher'] = 'OSGeo China Chapter'
    mrec.add_or_update(out_dic, force=True)


def run_export():
    all_recs = MPost.query_all(kind='9', limit=10000)
    for postinfo in all_recs:
        insert_into_db(postinfo)


if __name__ == '__main__':
    run_export()
