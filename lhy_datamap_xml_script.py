'''
通过Data中相关图层名称获取url，并通过url获取xml数据
'''
import json
import sys
from xml.etree import ElementTree

import yaml
from owslib.wms import WebMapService


def get_xml(maplayers):
    with open("./demo_mapproxy.yaml", encoding='utf-8') as file:
        content = file.read()
        print(maplayers)
        # 设置Loader=yaml.FullLoader忽略YAMLLoadWarning警告
        data = yaml.load(content, Loader=yaml.FullLoader)

        for ii in data['layers']:
            if ii['name'] == maplayers:
                mapurl = ii[maplayers]['req']['url']

                wms = WebMapService(mapurl, version='1.3.0')
                result = wms.getServiceXML()

                result = str(result)[2:-1]
                result2 = "".join(json.dumps(result).split("\\n"))
                result3 = "".join(json.dumps(result2).split("\\"))
                print(result3[2:-2])


if __name__ == '__main__':
    maplayers = sys.argv[1]
    # maplayers = "q_daan_soil_salinization_SS_2015_mn0007"

    get_xml(maplayers)
