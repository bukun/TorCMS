# -*- coding:utf-8 -*-

"""
create YAML file  for MapProxy.
"""

import sys

sys.path.append('')
from pathlib import Path

import pytest
import requests
import yaml

try:
    from osgeo import ogr, osr
    from owslib.wms import WebMapService
    from shapely import wkt
except:
    pass

from torcms.core.tools import logger
from torcms.model.category_model import MCategory
from torcms.model.post2catalog_model import MPost2Catalog
from torcms.model.post_model import MPost

out_rst_dir = Path("static/map_legend")

tmpl_file = Path(__file__).parent / 'tmpl_wms.html'

tmpl = open(tmpl_file).read()


@pytest.mark.skip(reason="跳过测试函数的测试case")
def update_category(uid, post_data):
    """
    Update the category of the post.
    :param uid:  The ID of the post. Extra info would get by requests.
    """

    # deprecated
    # catid = kwargs['catid'] if MCategory.get_by_uid(kwargs.get('catid')) else None
    # post_data = self.get_request_arguments()

    """
    在前端，使用 `gcat0`，`gcat1`，`gcat2` 等，作为分类的参数。
    因为一个 post 可能会有多个分类，再定义第1分类的 key ：
        'def_cat_uid'： 第1分类
        'def_cat_pid' : 分1分类的父类
    """
    if "gcat0" in post_data:
        pass
    else:
        return False

    # Used to update MPost2Category, to keep order.
    the_cats_arr = []
    # Used to update post extinfo.
    the_cats_dict = {}

    # for old page. deprecated
    # def_cate_arr.append('def_cat_uid')

    def_cate_arr = ["gcat{0}".format(x) for x in range(10)]
    for key in def_cate_arr:
        if key not in post_data:
            continue
        if post_data[key] == "" or post_data[key] == "0":
            continue
        # 有可能选重复了。保留前面的
        if post_data[key] in the_cats_arr:
            continue

        the_cats_arr.append(post_data[key] + " " * (4 - len(post_data[key])))
        the_cats_dict[key] = post_data[key] + " " * (4 - len(post_data[key]))

    # if catid:
    #     def_cat_id = catid
    if the_cats_arr:
        def_cat_id = the_cats_arr[0]
    else:
        def_cat_id = None

    if def_cat_id:
        the_cats_dict["gcat0"] = def_cat_id
        the_cats_dict["def_cat_uid"] = def_cat_id
        the_cats_dict["def_cat_pid"] = MCategory.get_by_uid(def_cat_id).pid

    logger.info("Update category: {0}".format(the_cats_arr))
    logger.info("Update category: {0}".format(the_cats_dict))

    # Add the category
    MPost.update_jsonb(uid, the_cats_dict)

    for index, idx_catid in enumerate(the_cats_arr):
        MPost2Catalog.add_record(uid, idx_catid, index)

    # Delete the old category if not in post requests.
    current_infos = MPost2Catalog.query_by_entity_uid(uid, kind="").objects()
    for cur_info in current_infos:
        if cur_info.tag_id not in the_cats_arr:
            MPost2Catalog.remove_relation(uid, cur_info.tag_id)


@pytest.mark.skip(reason="跳过测试函数的测试case")
def trans(bnd_box):
    source = osr.SpatialReference()
    epsg_code = int(bnd_box[-1].split(":")[-1])
    print(bnd_box)
    print(epsg_code)
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

    print(type(ll), ll.y, ll.x, type(ur), ur.y, ur.x)

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


@pytest.mark.skip(reason="跳过测试函数的测试case")
def test_parse_proxy():
    yaml_file = Path(__file__).parent / 'pub_maproxy.yaml'
    map_dict = yaml.load(open(yaml_file), Loader=yaml.FullLoader)

    for cache_sig, val in map_dict["caches"].items():
        if "osm_cache" in cache_sig:
            continue
        print("=" * 40)
        # print(cache_sig)
        src_sig = val["sources"][0]
        qfile_url = map_dict["sources"][src_sig]["req"]["url"]
        qfile_lyrs = map_dict["sources"][src_sig]["req"]["layers"]
        qfile_path = qfile_url.split("=")[-1]

        print(qfile_url)
        print(qfile_lyrs)
        print(qfile_path)

        try:
            wms = WebMapService(qfile_url, version="1.3.0")
        except:
            # time.sleep(5)
            # wms = WebMapService(qfile_url, version='1.3.0')
            continue

        wms_lyr = wms[qfile_lyrs]

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
            req_str = "{}&LAYER={}&FORMAT=image/png&STYLE=default&SERVICE=WMS&VERSION=1.3.0&REQUEST=GetLegendGraphic&FORMAT=image/png&STYLE=&SLD_VERSION=1.1.0".format(
                qfile_url, qfile_lyrs
            )
            print("fetching legend ...")
            print(req_str)
            r = requests.get(req_str, stream=True)
            if r.status_code == 200:
                with open(legend_img_file, "wb") as f:
                    for chunk in r.iter_content(1024):
                        f.write(chunk)

        uid = "v" + str(cache_sig)[2:]
        post_data = {
            "title": wms[qfile_lyrs].title,
            "cnt_md": abstract,
            "kind": "v",
            "gcat0": "v101",
            "user_name": "admin",
            "valid": 1,
        }
        catid = post_data["gcat0"]
        ext_data = {
            "ext_data-maplet": cache_sig,
            "ext_lat": bnd_box[0],
            "ext_lon": bnd_box[1],
            "ext_zoom_current": bnd_box[2],
            "ext_zoom_min": bnd_box[3],
            "ext_zoom_max": bnd_box[4],
            "ext_qfile_path": qfile_path,
            "def_uid": uid,
            "gcat0": catid,
            "def_cat_uid": catid,
            "def_cat_pid": catid[:2] + "00",
        }

        MPost.add_or_update_post(uid, post_data, ext_data)
        update_category(uid, post_data)
        MPost2Catalog.add_record(uid, catid)


#    parse_proxy()
