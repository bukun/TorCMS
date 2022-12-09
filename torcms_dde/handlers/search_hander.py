import tornado.web
import tornado.escape
from torcms.core.base_handler import BaseHandler
from owslib.csw import CatalogueServiceWeb
from owslib.fes import PropertyIsEqualTo, PropertyIsLike, BBox


class DirectorySearchHandler(BaseHandler):
    def initialize(self):
        super(DirectorySearchHandler, self).initialize()

    def get(self, url_str=''):

        if len(url_str) > 0:
            url_arr = url_str.split('/')
            # if url_str == '':
            # self.render('metadata/meta_index.html')
        if url_str == '':
            self.list('')
        elif url_arr[0] == 'search':
            self.search(url_arr[1], url_arr[2])

        elif url_arr[0] == 'view':
            self.ajax_get(url_arr[1])

    # def post(self, url_str=''):
    #     print('vvsdlfksdajfsaklfjsdlfsjdfsadlkfjsadlkfsd')
    #     post_data = {}
    #     print(self.request.arguments)
    #     for key in self.request.arguments:
    #         print(key)
    #         post_data[key] = self.get_arguments(key)
    #     self.get_result(post_data)

    # def search(self, keyw):
    #     # print('====' * 40)
    #     # print(post_data)
    #     url = 'http://meta.osgeo.cn/pycsw/csw.py?mode=sru&operation=searchRetrieve&query={0}
    # &maximumRecords=5&startRecord=5&outputFormat=application/json'.format(
    #         keyw)
    #     r = requests.get(url)
    #     pprint.pprint(r.text)
    #     self.parseXML(r.text.encode(encoding='UTF-8'))
    def list(self, keyw):
        # print('====' * 40)
        # print(post_data)
        keyw = 'data'
        csw = CatalogueServiceWeb('https://drr.ikcest.org/csw')
        birds_query_like = PropertyIsLike('dc:title', '%{0}%'.format(keyw))
        csw.getrecords2(constraints=[birds_query_like], maxrecords=20)
        print('-' * 20)
        print(csw.results)

        for rec in csw.results:
            print(rec)

        # out_dic = {}
        # for rec in csw.records:
        # url = 'http://meta.osgeo.cn/pycsw/csw.py?mode=sru&operation=searchRetrieve&query={0}\
        # maximumRecords=5&startRecord=5&outputFormat=application/json'.format(
        #     keyw)
        # r = requests.get(url)
        # pprint.pprint(r.text)

        self.render('../torcms_dde/search/meta_index.html',
                    meta_results=csw.records,
                    userinfo=self.userinfo)

        # self.parseXML(r.text.encode(encoding='UTF-8'))

    def search(self, keyw, isweb):
        # print('====' * 40)
        # print(post_data)

        csw = CatalogueServiceWeb('https://drr.ikcest.org/csw')
        # birds_query_like = PropertyIsLike('dc:title', '%{0}%'.format(keyw))
        birds_query = PropertyIsLike('csw:AnyText', '%{0}%'.format(keyw))

        if isweb == '1':
            csw.getrecords2(constraints=[birds_query], maxrecords=20)
        else:
            csw.getrecords2(constraints=[birds_query], maxrecords=20, distributedsearch=True, hopcount=2)
        print('-' * 20)
        print(isweb)
        print(csw.results)

        for rec in csw.records:
            print(rec)

        # out_dic = {}
        # for rec in csw.records:

        # url = 'http://meta.osgeo.cn/pycsw/csw.py?mode=sru&operation=searchRetrieve&query={0}&
        # maximumRecords=5&startRecord=5&outputFormat=application/json'.format(
        #     keyw)
        # r = requests.get(url)
        # pprint.pprint(r.text)

        self.render('../torcms_dde/search/show_result.html',
                    meta_results=csw.records,
                    userinfo=self.userinfo,
                    isweb=isweb
                    )

        # self.parseXML(r.text.encode(encoding='UTF-8'))

    # def get_result(self, post_data):
    #     print('====' * 40)
    #     print(post_data)
    #     url = 'http://meta.osgeo.cn/pycsw/csw.py?mode=sru&operation=searchRetrieve&query={0}
    # &maximumRecords=5&startRecord=5'.format(
    #         post_data['keyw'][0])
    #     r = requests.get(url)
    #     pprint.pprint(r.text)
    #     self.parseXML(r.text.encode(encoding='UTF-8'))
    #     # data = urllib.request.Request(url)

    def ajax_get(self, uuid):
        print('=' * 20)
        print(uuid)
        # uuid = uuid.split(':')[-1]
        csw = CatalogueServiceWeb('https://drr.ikcest.org/csw')
        # birds_query_like = PropertyIsLike('dc:title', '%{0}%'.format(keyw))

        csw.getrecordbyid(id=[uuid])
        print('-' * 20)
        print(csw.results)
        out_dict = {
            'title': '',
            'uid': '',
            'sizhi': '',

        }

        self.render('../torcms_dde/search/show_rec.html',
                    kws=out_dict,
                    meta_rec=csw.records.get(uuid),
                    unescape=tornado.escape.xhtml_unescape,
                    userinfo=self.userinfo
                    )

        # #
        # def parseXML(self, data):
        #
        #     tree = etree.fromstring(data)
        #     # root = tree.getroot()
        #     uu = tree.findall('zs:record', tree.nsmap)
        #
        #     meta_arr = []
        #     for x in uu:
        #         meta_arr.append(MyXML(x))
        #         # print(x.element('ows:LowerCorner'))
        #         # uu = etree.SubElement(x, "LowerCorner")
        #         # for sub_ele in  x.iter():
        #         #     print(sub_ele.tag)
        #         #     if 'title' == sub_ele.tag.split('}')[1]:
        #         #         print(sub_ele.text)
        #         #     if 'LowerCorner' ==  sub_ele.tag.split('}')[1]:
        #         #         print(sub_ele.text)
        #
        #     self.render('metadata/show_result.html',
        #                 meta_arr=meta_arr)


class MyXML():
    def __init__(self, in_ele):
        self.element = in_ele

    def uid(self):
        for sub_ele in self.element.iter():
            if 'identifier' == sub_ele.tag.split('}')[1]:
                return sub_ele.text

    def recordPosition(self):
        for sub_ele in self.element.iter():
            if 'recordPosition' == sub_ele.tag.split('}')[1]:
                return sub_ele.text

    def sizhi(self):
        out_arr = [0, 0, 0, 0]
        for sub_ele in self.element.iter():
            if 'LowerCorner' == sub_ele.tag.split('}')[1]:
                t1 = sub_ele.text.split(' ')
                out_arr[0] = float(t1[0])
                out_arr[2] = float(t1[1])
            if 'UpperCorner' == sub_ele.tag.split('}')[1]:
                t2 = sub_ele.text.split(' ')
                out_arr[1] = float(t2[0])
                out_arr[3] = float(t2[1])
        return out_arr

    def title(self):
        for sub_ele in self.element.iter():
            if 'title' == sub_ele.tag.split('}')[1]:
                return sub_ele.text
