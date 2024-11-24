# -*- coding:utf-8 -*-

"""
create YAML file  for MapProxy.
"""

import sys

sys.path.append('.')
import yaml
from pathlib import Path
from shapely import wkt
from osgeo import osr, ogr
import requests
from owslib.wms import WebMapService
import os
import pathlib
import json
from openpyxl import load_workbook
from datetime import datetime

from cfg import DB_INFO

out_rst_dir = Path("static/map_legend")

tmpl_file = Path(__file__).parent / 'test_qgis_svr/tmpl_wms.html'

tmpl = open(tmpl_file).read()
import psycopg2

## 连接到一个给定的数据库
conn = psycopg2.connect(database=DB_INFO['NAME'], user=DB_INFO['USER'], password=DB_INFO['PASSWORD'],
                        host=DB_INFO['HOST'], port=DB_INFO['PORT'])
## 建立游标，用来执行数据库操作
cursor = conn.cursor()


def trans(bnd_box):
    source = osr.SpatialReference()
    epsg_code = int(bnd_box[-1].split(":")[-1])
    # print(bnd_box)
    # print(epsg_code)
    source.ImportFromEPSG(epsg_code)

    target = osr.SpatialReference()
    target.ImportFromEPSG(4326)

    transform = osr.CoordinateTransformation(source, target)

    if epsg_code == 4326:
        ll = f"POINT ({bnd_box[1]} {bnd_box[0]})"
        ur = f"POINT ({bnd_box[3]} {bnd_box[2]})"

    else:
        point = ogr.CreateGeometryFromWkt(f"POINT ({bnd_box[0]} {bnd_box[1]})")
        point.Transform(transform)
        ll = point.ExportToWkt()

        point = ogr.CreateGeometryFromWkt(f"POINT ({bnd_box[2]} {bnd_box[3]})")
        point.Transform(transform)
        ur = point.ExportToWkt()

    ll = wkt.loads(ll)
    ur = wkt.loads(ur)

    xx = ur.x - ll.x
    yy = ur.y - ll.y

    # print(type(ll), ll.y, ll.x, type(ur), ur.y, ur.x)

    if xx > 160:
        zoom_cur = 1
    elif xx > 80:
        zoom_cur = 2
    elif xx > 40:
        zoom_cur = 3
    elif xx > 20:
        zoom_cur = 4
    elif xx > 10:
        zoom_cur = 5
    elif xx > 5:
        zoom_cur = 6
    elif xx > 2.5:
        zoom_cur = 7
    elif xx > 1.2:
        zoom_cur = 8
    elif xx > 0.6:
        zoom_cur = 9
    elif xx > 0.3:
        zoom_cur = 10
    elif xx > 0.15:
        zoom_cur = 11
    else:
        zoom_cur = 12
    zoom_min = zoom_cur - 4
    zoom_max = zoom_cur + 5

    return ((ll.x + ur.x) / 2, (ll.y + ur.y) / 2, zoom_cur, zoom_min, zoom_max)


def test_parse_proxy():
    # yaml_file = Path(__file__).parent / 'test_qgis_svr/xx_qsvr_mapproxy.yaml'
    yaml_file = '/tmp/xx_qsvr_mapproxy.yaml'

    if os.path.exists(yaml_file):
        pass
    else:
        print('yaml文件不存在')
        return False

    try:
        map_dict = yaml.load(open(yaml_file), Loader=yaml.FullLoader)
    except:
        print('yaml.load异常')
        return False
    err_list = []
    for cache_sig, val in map_dict["caches"].items():
        if "osm_cache" in cache_sig:
            continue

        # print(cache_sig)

        src_sig = val["sources"][0]
        qfile_url = map_dict["sources"][src_sig]["req"]["url"]
        qfile_lyrs = map_dict["sources"][src_sig]["req"]["layers"]

        query = "select * from qgismap where layer_name=%s"
        params = (qfile_lyrs,)  # 根据需求设置查询条件的值

        cursor.execute(query, params)

        if cursor.fetchone():
            continue

        qfile_path = qfile_url.split("=")[-1]
        host = qfile_url.split("/")[2]

        try:
            wms = WebMapService(qfile_url, version="1.3.0")

            wms_lyr = wms[qfile_lyrs]

        except Exception as e:  # 未知异常的兜底方案
            print("有问题数据：")
            print("错误信息:", e)

            print(qfile_url)
            print(qfile_lyrs)
            err_list.append({'error': str(e), 'url': qfile_url, 'layer': qfile_lyrs})
            continue

        # print(wms[qfile_lyrs].title)

        abstract = wms[qfile_lyrs].abstract
        if abstract:
            pass
        else:
            abstract = """这里是摘要说明。进行测试。
                """

        bnd_box = trans(wms_lyr.boundingBox)

        if out_rst_dir.exists():
            pass
        else:
            out_rst_dir.mkdir(parents=True)
        legend_img_file = out_rst_dir / f"xx_{cache_sig}.png"
        if legend_img_file.exists():
            pass
        else:
            req_str = "{}&LAYERS={}&FORMAT=image/png&STYLE=default&SERVICE=WMS&VERSION=1.3.0&REQUEST=GetLegendGraphic&FORMAT=image/png&STYLE=&SLD_VERSION=1.1.0".format(
                qfile_url, qfile_lyrs
            )
            # print("fetching legend ...")
            # print(req_str)
            r = requests.get(req_str, stream=True)
            if r.status_code == 200:
                with open(legend_img_file, "wb") as f:
                    for chunk in r.iter_content(1024):
                        f.write(chunk)

        pp_data = {
            "title": wms[qfile_lyrs].title,
            "cnt_md": abstract,
            "user_name": "admin",
            "ext_data-maplet": cache_sig,
            "ext_lat": bnd_box[0],
            "ext_lon": bnd_box[1],
            "ext_zoom_current": bnd_box[2],
            "ext_zoom_min": bnd_box[3],
            "ext_zoom_max": bnd_box[4],
            "ext_qfile_path": qfile_path,

            "qfile_url": qfile_url,
            "qfile_lyrs": qfile_lyrs,
            "map_id": cache_sig,
            "host": host,
        }

        sql = """insert into qgismap (title,cnt_md, lat,lon,zoom_current,zoom_min,zoom_max,layer_name,url,path,host,name,mapid,create_time,update_time,date) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
        para = (
            pp_data['title'], pp_data['cnt_md'], pp_data['ext_lat'], pp_data['ext_lon'],
            pp_data['ext_zoom_current'], pp_data['ext_zoom_min'],
            pp_data['ext_zoom_max'], pp_data['qfile_lyrs'], pp_data['qfile_url'], pp_data['ext_qfile_path'],
            pp_data['host'], pp_data['qfile_lyrs'], pp_data['map_id'], datetime.now(), datetime.now(), datetime.now())
        cursor.execute(sql, para)
        conn.commit()

    with open("xx_qgismap_err_list.json", "w") as file:
        err_list.append({"数量": len(err_list)})
        json.dump(err_list, file, ensure_ascii=False)
    print("未入库数据已写入xx_qgismap_err_list.json")


if __name__ == '__main__':
    test_parse_proxy()
