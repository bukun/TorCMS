from pprint import pprint
import requests

dict = {
    'title': 'Debian 11，最好的开源GIS系统即将发布',
    'text': '免费Jupyter科学计算服务，OSGeo中国中心发布免费Jupyter科学计算服务，OSGeo中国中心发布免费Jupyter科学计算服务，OSGeo中国中心发布免费Jupyter科学计算服务，OSGeo中国中心发布免费Jupyter科学计算服务，OSGeo中国中心发布'
}

r = requests.post("http://39.100.72.56:6625/data/j_get_tag", json=dict)
# print(r.status)
pprint(r.json())
