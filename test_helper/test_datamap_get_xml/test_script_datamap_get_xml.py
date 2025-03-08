'''
通过Data中相关图层名称获取url，并通过url获取xml数据
'''
import json
import sys
from pathlib import Path

import pytest
import yaml

try:
    from owslib.wms import WebMapService
except:
    pass
    # sys.exit()


@pytest.mark.skip(reason="跳过测试函数的测试case")
def test_get_xml():
    # maplayers = sys.argv[1]
    maplayers = "q_ht_geomor_geomor_mn1011"
    yaml_file = Path(__file__).parent / 'mapproxy.yaml'
    with open(yaml_file, encoding='utf-8') as file:
        content = file.read()

        # 设置Loader=yaml.FullLoader忽略YAMLLoadWarning警告
        data = yaml.load(content, Loader=yaml.FullLoader)

        for ii in data['layers']:
            if ii['name'] == maplayers:
                mapurl = ii[maplayers]['req']['url']
                try:
                    wms = WebMapService(mapurl, version='1.3.0')
                    result = wms.getServiceXML()

                    result = str(result)[2:-1]
                    result2 = "".join(json.dumps(result).split("\\n"))
                    result3 = "".join(json.dumps(result2).split("\\"))
                    print(result3[2:-2])
                except:
                    print("err")
