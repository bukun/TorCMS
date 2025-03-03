# -*- coding: utf-8

'''
导入数据集IMG
'''

import os
import sys

import geojson
from geojson import Feature, MultiPoint, MultiPolygon, Polygon

sys.path.extend('.')

from shapely.geometry import shape

from torcms.model.post_model import MPost


def import_meta():
    # 此文件夹下声明系统中的数据集及分类
    recs = MPost.query_all(kind='d', limit=10000)
    index = 0
    g_arr = []
    c_arr = []
    for rec in recs:
        _gson = rec.extinfo.get('geojson')
        if _gson:
            print('-' * 40)
            index = index + 1
            print('got', index)
            print(_gson)
            print(type(_gson))
            gson = geojson.loads(str(_gson).replace("'", '"'))
            print(type(gson))
            print(dir(gson))
            g_arr.append(gson)

            shape_poly = shape(gson)
            ct = shape_poly.centroid
            print(shape_poly)
            print(ct)

            feature_json = geojson.Point((ct.x, ct.y))
            print(feature_json)

            c_arr.append(feature_json)
            print(c_arr)
            # sys.exit()

    result = MultiPolygon(g_arr)

    result_ct = MultiPoint(c_arr)

    print(type(result))
    print(result)

    with open('xx_json.json', 'w') as fo:
        geojson.dump(result, fo)

    with open('xx_pt.json', 'w') as fo:
        geojson.dump(result_ct, fo)


if __name__ == '__main__':
    import_meta()
    print(os.getcwd())
