# -*- coding: utf-8 -*-

import os
import sys
import zipfile
import urllib.request


den_dir = './static/f2elib'

if os.path.exists(den_dir):
    pass
else:
    os.mkdir(den_dir)

def fetch_file(url, filename ):

    outfile = os.path.join(den_dir, filename)
    if os.path.exists(outfile):
        print('Exists: ', outfile)
        return True
    print('fetch ...')
    print(' ' * 4 + url)

    urllib.request.urlretrieve(url, outfile)
    zip_file = outfile
    f = zipfile.ZipFile(zip_file, 'r')
    for zfile in f.namelist():
        f.extract(zfile, den_dir)


def get_jquery():
    # jquery_url = 'https://code.jquery.com/jquery-3.1.1.min.js'
    jquery_url = 'http://r.osgeo.cn/f2elib/jquery.zip'
    qian, hou = os.path.split(jquery_url)
    fetch_file(jquery_url, hou)

def get_leaflet():
    leaflet_url = 'http://r.osgeo.cn/f2elib/leaflet_1.0.1.zip'
    qian, hou = os.path.split(leaflet_url)
    fetch_file(leaflet_url, hou)


def get_bootstrap():
    leaflet_url = 'http://r.osgeo.cn/f2elib/bootstrap_3.3.7.zip'
    qian, hou = os.path.split(leaflet_url)
    fetch_file(leaflet_url, hou)

def get_js_valid():
    leaflet_url = 'http://r.osgeo.cn/f2elib/jquery-validation_1.15.0.zip'
    qian, hou = os.path.split(leaflet_url)
    fetch_file(leaflet_url, hou)
def get_codemirror():
    leaflet_url = 'http://r.osgeo.cn/f2elib/codemirror_5.19.0.zip'
    qian, hou = os.path.split(leaflet_url)
    fetch_file(leaflet_url, hou)
def get_jqueryui():
    leaflet_url = 'http://r.osgeo.cn/f2elib/jqueryui_1.12.1.zip'
    qian, hou = os.path.split(leaflet_url)
    fetch_file(leaflet_url, hou)

def get_rating():
    leaflet_url = 'http://r.osgeo.cn/f2elib/bootstrap-star-rating-master.zip'
    qian, hou = os.path.split(leaflet_url)
    fetch_file(leaflet_url, hou)
def get_magnific():
    leaflet_url = 'http://r.osgeo.cn/f2elib/magnific-popup_1.1.0.zip'
    qian, hou = os.path.split(leaflet_url)
    fetch_file(leaflet_url, hou)


def get_ol3():

    # ol3_url = 'https://github.com/openlayers/ol3/releases/download/v3.18.2/v3.18.2-dist.zip'

    # qian, hou = os.path.split(ol3_url)
    # fetch_file(ol3_url, hou, outdir='ol3')

    tdir = os.path.join(den_dir, 'ol3')
    if os.path.exists(tdir):
        pass
    else:
        os.mkdir(tdir)

    ol3_css  = 'http://cdn.bootcss.com/ol3/3.18.2/ol.css'
    fetch_file(ol3_css, 'ol3/ol.css')


    ol3_js = 'http://cdn.bootcss.com/ol3/3.18.2/ol.js'
    fetch_file(ol3_js, 'ol3/ol.js')

def run_fetch_f2elib():
    get_jqueryui()
    get_codemirror()
    get_js_valid()
    get_leaflet()
    get_jquery()
    # get_ol3()
    get_bootstrap()
    get_rating()
    get_magnific()




