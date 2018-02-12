# -*- coding: utf-8 -*-

'''
Download the f2e libs from internet.
'''

import os
import zipfile
import urllib.request

OUT_PATH = './static/f2elib'

if os.path.exists(OUT_PATH):
    pass
else:
    os.mkdir(OUT_PATH)


def fetch_file(url, filename):
    '''
    Feting the file.
    '''
    outfile = os.path.join(OUT_PATH, filename)
    if os.path.exists(outfile):
        # print('Exists: ', outfile)
        return True
    print('fetch ...')
    print(' ' * 4 + url)

    urllib.request.urlretrieve(url, outfile)
    zip_file = outfile
    zfile_enum = zipfile.ZipFile(zip_file, 'r')
    for zfile in zfile_enum.namelist():
        zfile_enum.extract(zfile, OUT_PATH)


def get_jquery():
    '''
    Get JQuery library.
    '''
    jquery_url = 'http://r.osgeo.cn/f2elib/jquery.zip'
    fetch_file(jquery_url, os.path.split(jquery_url)[1])


def get_leaflet():
    '''
    Get LeafletJS library.
    '''
    leaflet_url = 'http://r.osgeo.cn/f2elib/leaflet_1.2.0.zip'
    fetch_file(leaflet_url, os.path.split(leaflet_url)[1])


def get_bootstrap():
    '''
    Get BootStrop CSS library.
    '''
    leaflet_url = 'http://r.osgeo.cn/f2elib/bootstrap_3.3.7.zip'
    fetch_file(leaflet_url, os.path.split(leaflet_url)[1])


def get_js_valid():
    '''
    Get JQuery-Validation library.
    '''
    leaflet_url = 'http://r.osgeo.cn/f2elib/jquery-validation_1.15.0.zip'
    fetch_file(leaflet_url, os.path.split(leaflet_url)[1])


def get_codemirror():
    '''
    Get CodeMirror JavaScript library.
    '''
    leaflet_url = 'http://r.osgeo.cn/f2elib/codemirror_5.25.0.zip'
    fetch_file(leaflet_url, os.path.split(leaflet_url)[1])


def get_jqueryui():
    '''
    Get JQueryUI library.
    '''
    leaflet_url = 'http://r.osgeo.cn/f2elib/jqueryui_1.12.1.zip'
    fetch_file(leaflet_url, os.path.split(leaflet_url)[1])


def get_rating():
    '''
    Get BootStrop Star Rating library.
    '''
    leaflet_url = 'http://r.osgeo.cn/f2elib/bootstrap-star-rating-master.zip'
    fetch_file(leaflet_url, os.path.split(leaflet_url)[1])


def get_magnific():
    '''
    Get Magnific PopUp JavaScript library.
    '''
    leaflet_url = 'http://r.osgeo.cn/f2elib/magnific-popup_1.1.0.zip'
    fetch_file(leaflet_url, os.path.split(leaflet_url)[1])


def get_ol3():
    '''
    Get OpenLayers3 JavaScript library.
    :return: None
    '''
    # ol3_url = 'https://github.com/openlayers/ol3/releases/download/v3.18.2/v3.18.2-dist.zip'
    # qian, hou = os.path.split(ol3_url)
    # fetch_file(ol3_url, hou, outdir='ol3')

    tdir = os.path.join(OUT_PATH, 'ol3')
    if os.path.exists(tdir):
        pass
    else:
        os.mkdir(tdir)

    ol3_css = 'http://cdn.bootcss.com/ol3/3.18.2/ol.css'
    fetch_file(ol3_css, 'ol3/ol.css')

    ol3_js = 'http://cdn.bootcss.com/ol3/3.18.2/ol.js'
    fetch_file(ol3_js, 'ol3/ol.js')


def run_f2elib(*args):
    '''
    Get All the libraries.
    :param args: 
    :return: None
    '''
    get_jqueryui()
    get_codemirror()
    get_js_valid()
    get_leaflet()
    get_jquery()
    # get_ol3()
    get_bootstrap()
    get_rating()
    get_magnific()
