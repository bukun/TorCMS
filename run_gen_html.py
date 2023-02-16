# -*- coding:utf-8 -*-

'''
create YAML file  for MapProxy.
'''
import sys
from pprint import pprint
import os
import yaml
import re
from pathlib import Path
from shapely import wkt

from osgeo import osr, ogr
import requests
import time

from owslib.wms import WebMapService

out_rst_dir = Path('source/xx_rst')

tmpl = open('tmpl_wms.html').read()

TPL_MAPPROXY = '''
services:
  demo:
  tms:
    use_grid_names: true
    # origin for /tiles service
    origin: 'nw'
  kml:
      use_grid_names: true
  wmts:
  wms:
    md:
      title: MapProxy WMS Proxy
      abstract: This is a minimal MapProxy example.
layers:
  - name: osm
    title: Omniscale OSM WMS - osm.omniscale.net
    sources: [osm_cache]

caches:
  osm_cache:
    grids: [webmercator]
    sources: [osm_wms]

sources:
  osm_wms:
    type: wms
    req:
      # use of this source is only permitted for testing
      url: http://osm.omniscale.net/proxy/service?
      layers: osm

grids:
    webmercator:
        base: GLOBAL_WEBMERCATOR

globals:
'''

def gen_sec_index():
    for xx in out_rst_dir.rglob('sec*'):
        print(xx)
        rst_list = []
        for yy in xx.iterdir():
            if yy.name.startswith('pub'):
                rst_list.append(yy.name)
        rst_list.sort()
        with open(xx / 'index.rst', 'w') as fo:
            fo.write(xx.name + '\n')
            fo.write('=' * 80 + '\n')
            fo.write('\n\n')
            fo.write('''
.. toctree::
   :maxdepth: 1

''')

            for ii in rst_list:
                fo.write(' ' * 3 + ii + '\n')


def trans(bnd_box):
    
    
    source = osr.SpatialReference()
    epsg_code = int(bnd_box[-1].split(':')[-1])
    print(bnd_box)
    print(epsg_code)
    source.ImportFromEPSG(epsg_code)
    
    target = osr.SpatialReference()
    target.ImportFromEPSG(4326)
    
    transform = osr.CoordinateTransformation(source, target)

    if epsg_code == 4326:
        ll = f"POINT ({bnd_box[1]} {bnd_box[0]})"
        ur  = f"POINT ({bnd_box[3]} {bnd_box[2]})"


    else:
        point = ogr.CreateGeometryFromWkt(f"POINT ({bnd_box[0]} {bnd_box[1]})")
        point.Transform(transform)
        ll  = point.ExportToWkt()

        point = ogr.CreateGeometryFromWkt(f"POINT ({bnd_box[2]} {bnd_box[3]})")
        point.Transform(transform)
        ur = point.ExportToWkt()


    ll = wkt.loads(ll)
    ur = wkt.loads(ur)

    xx = ur.x - ll.x
    yy = ur.y - ll.y

    print(type(ll), ll.y, ll.x, type(ur),ur.y, ur.x)

    if xx > 160:
        zoom_cur = 1
    elif xx > 80:
        zoom_cur = 2
    elif xx > 40:
        zoom_cur = 3
    elif xx > 20:
        zoom_cur = 4
    elif xx > 10:
        zoom_cur =5 
    elif xx > 5:
        zoom_cur = 6
    elif xx > 2.5:
        zoom_cur =7 
    elif xx > 1.2:
        zoom_cur =8 
    elif xx > .6:
        zoom_cur = 9
    elif xx > .3:
        zoom_cur = 10
    elif xx > .15:
        zoom_cur = 11
    else:
        zoom_cur = 12
    zoom_min = zoom_cur - 4
    zoom_max = zoom_cur + 5

    return ((ll.x + ur.x) / 2 , (ll.y +  ur.y) / 2 , zoom_cur, zoom_min, zoom_max )

def gen_ch_index():
    for xx in out_rst_dir.iterdir():
        rst_list = []
        if xx.name.startswith('ch'):
            print(xx)
        for yy in xx.iterdir():
            if yy.name.startswith('sec'):
                rst_list.append(yy.name)
        rst_list.sort()
        with open(xx / 'index.rst', 'w') as fo:
            fo.write(xx.name + '\n')
            fo.write('=' * 80 + '\n')
            fo.write('\n\n')
            fo.write('''
.. toctree::
   :maxdepth: 1

''')

            for ii in rst_list:
                fo.write(' ' * 3 + ii + '/index.rst\n')


def gen_index():
    rst_list = []
    for xx in out_rst_dir.iterdir():

        if xx.name.startswith('ch'):
            print(xx)
            rst_list.append(xx.name)

    with open('source/index.rst', 'w') as fo:
        fo.write('''giSphinx 地图集项目演示
===========================

基于Sphinx文档工具发布QGIS制图结果地图。
        
.. toctree::
   :maxdepth: 1
   :numbered: 2

''')

        for ii in rst_list:
            fo.write(f'   xx_rst/{ii}/index\n')


def parse_proxy():
    map_dict = yaml.load(open('xx_demo_mapproxy.yaml'), Loader=yaml.FullLoader)

    for cache_sig, val in map_dict['caches'].items():
        if 'osm_cache' in cache_sig:
            continue
        print('=' * 40)
        # print(cache_sig)
        src_sig = val['sources'][0]
        qfile_url = map_dict['sources'][src_sig]['req']['url']
        qfile_lyrs = map_dict['sources'][src_sig]['req']['layers']
        qfile_path = qfile_url.split('=')[-1]

        print(qfile_url)
        print(qfile_lyrs)
        print(qfile_path)
        
        try:
            wms = WebMapService(qfile_url, version='1.3.0')
        except:
            # time.sleep(5)
            # wms = WebMapService(qfile_url, version='1.3.0')
            continue
        wms_lyr =  wms[qfile_lyrs]

        print(wms[qfile_lyrs].title)

        abstract = wms[qfile_lyrs].abstract
        if abstract:
            pass
        else:
            abstract = '''这里是摘要说明。进行测试。
            '''
        # print(abstract)
        # print(dir(wms[qfile_lyrs]))
        # print(wms_lyr.boundingBox)
        # print(wms_lyr.dimensions)

        bnd_box = trans(wms_lyr.boundingBox)
        # continue

        # sys.exit()

        ch_sig_arr = re.findall("\/ch\d\d", qfile_path)
        sec_sig_arr = re.findall("\/sec\d\d", qfile_path)


        if ch_sig_arr:
            ch_sig = ch_sig_arr[0][1:]
        else:
            ch_sig = 'chxx'

        if sec_sig_arr:
            sec_sig = sec_sig_arr[0][1:]
        else:
            sec_sig = 'secxx'


       v
        with open(rst_out_file, 'w') as fo:
            fo.write(wms[qfile_lyrs].title)
            fo.write('\n')
            fo.write('=' * 80 + '\n\n')
            fo.write(abstract)
            fo.write('\n' * 2)
            fo.write(f'''
.. raw:: html

   <div id="map_kd1" data-maplet="{cache_sig}" data-title="{wms[qfile_lyrs].title}" data-x={bnd_box[0]} data-y={bnd_box[1]} data-cur={bnd_box[2]} data-min={bnd_box[3]}  data-max={bnd_box[4]}></div>
''')
            fo.write('\n' * 2)

            fo.write('Legend:\n')
            fo.write('-' * 80 + '\n')

            fo.write(f'''
.. image:: ./xx_{cache_sig}.png

''')
            fo.write('\n' * 2)
            fo.write('Information:\n')
            fo.write('-' * 80 + '\n')

            fo.write(f'**Path**: {qfile_path}\n')
            fo.write('\n' * 2)
            fo.write(f'**Layer ID**: {cache_sig}\n')
            fo.write('\n' * 2)
            fo.write(f'**Center**: {bnd_box[0]}, {bnd_box[1]}\n')
            fo.write('\n' * 2)
            fo.write(f'**Zoom**: {bnd_box[2]}\n')


            legend_img_file = pp / f'xx_{cache_sig}.png'
            if legend_img_file.exists():
                pass
            else:
                req_str = '{}&LAYER={}&FORMAT=image/png&STYLE=default&SERVICE=WMS&VERSION=1.3.0&REQUEST=GetLegendGraphic&FORMAT=image/png&STYLE=&SLD_VERSION=1.1.0'.format(
                    qfile_url,
                    qfile_lyrs
                )
                print('fetching legend ...')
                print(req_str)
                r = requests.get(req_str, stream=True)
                if r.status_code == 200:
                    with open(legend_img_file, 'wb') as f:
                        for chunk in r.iter_content(1024):
                            f.write(chunk)


if __name__ == '__main__':
    parse_proxy()
