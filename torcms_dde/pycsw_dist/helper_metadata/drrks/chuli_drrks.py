'''
DRRKS本身数据集
'''
from pprint import pprint
import sys; sys.path.append('.')
import os

from torcms.model.post_model import MPost
import yaml
# import ruamel.yaml

'''
解析DRR数据集，解压缩后获取每个的地理范围
'''

import tornado.escape
import os
from pathlib import Path
from osgeo import ogr
import fiona
from pyproj import Proj
from pyproj import CRS
from osgeo import osr
import shutil
# import subprocess
# import nltk

from  dehtml import dehtml

from bs4 import BeautifulSoup



target = osr.SpatialReference()
target.ImportFromEPSG(4326)

inws = Path('/pb1/drr_datasets')

workdir = Path('/vb1/tmp')


tmpl = open('./tmpl.xml').read()

# print(tmpl)

tmpl_0 = '''<?xml version="1.0" encoding="UTF-8"?>
<csw:Record
	xmlns:csw="http://www.opengis.net/cat/csw/2.0.2"
	xmlns:dc="http://purl.org/dc/elements/1.1/"
	xmlns:dct="http://purl.org/dc/terms/"
	xmlns:ows="http://www.opengis.net/ows"
	xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
	xsi:schemaLocation="http://www.opengis.net/cat/csw/2.0.2/record.xsd">
'''

tmpl_9 = '''
</csw:Record>
'''

tp_creator = '<dc:creator>{}</dc:creator>'
tp_contributor = '<dc:contributor>{}</dc:contributor>'
tp_publisher = '<dc:publisher>{}</dc:publisher>'
tp_subject = '<dc:subject>{}</dc:subject>'
tp_abstract = '<dct:abstract>{}</dct:abstract>'
tp_identifier = '<dc:identifier>{}</dc:identifier>'
tp_relation = '<dc:relation>{}</dc:relation>'
tp_source = '<dc:source>{}</dc:source>'
tp_rights = '<dc:rights>{}</dc:rights>'
tp_type = '<dc:type>{}</dc:type>'
tp_title = '<dc:title>{}</dc:title>'
tp_mofified = '<dct:modified>{}</dct:modified>'
tp_language = '<dc:language>{}</dc:language>'


def get_geo(wdir):
    a,b,c,d = -180, -90, 180, 90
    sig = False
    for wfile in wdir.rglob('*.shp'):
        sig = True
        print('    ', wfile)
        # ds = ogr.Open(str(wfile))
        # lyr = ds.GetLayer(0)
        # ext = lyr.GetExtent()
        # env = lyr.GetEnvelope()
        ds = fiona.open(wfile)


        # print(ds.crs)


        try:
            crs = CRS(ds.crs)
            # print('=' * 20)
            # print(type(crs))
            # print(crs)
            # print(type(target))
            # print(target)
        except:
            continue

        p = Proj(crs)
        # print(p)

        ll = p(ds.bounds[0], ds.bounds[1], inverse = True)
        ur  = p(ds.bounds[2], ds.bounds[3], inverse = True)
        # srcp = osr.SpatialReference()
        # srcp.ImportFromEPSG(int(ds.crs['init'].split(':')[-1]))
        # trans = osr.CoordinateTransformation(srcp, target)
        # ll = trans.TransformPoint(ds.bounds[0], ds.bounds[1])
        # ur = trans.TransformPoint(ds.bounds[2], ds.bounds[3])

        if ll[0] > 90 or ll[1] > 90 or ur[0] > 90 or ur[1] > 90:
            print(ds.bounds)
            print(ll, ur)

        if ll[0] > a:
            a = ll[0]
        if ll[1] > b:
            b = ll[1]
        if ur[0] < c:
            c = ur[0]
        if ur[1] < d:
            d = ur[1]

    if sig:
        return a,b,c,d
    else:
        return None


        # print(ext)
        # print(env)

def clean():
    for wfile in workdir.rglob('*'):
        if wfile.is_file():
            wfile.unlink()

def walk_dir(the_sig):
    os.chdir(workdir)

    for wfile in inws.rglob('*.7z'):

        if f'_dn{the_sig}' in wfile.name:

            clean()
            if wfile.exists():
                pass
            else:
                continue
            shutil.copy(wfile, workdir / wfile.name )
            file7z = workdir / wfile.name
            if file7z.exists():

                subprocess.run(['7z', 'x', f'{file7z}'])
                print('=' * 40)
                print(wfile)
                uu = get_geo(workdir)
                print(uu)
                return uu



def run_export():
    all_recs = MPost.query_all(kind='9', limit=10000)
    out_arr = []
    fout = open('xx_links.txt','w')
    for postinfo in all_recs:
        print('=' * 40)
        pid = postinfo.extinfo.get('def_cat_pid')
        print()
        if pid == '2200':
            pass
        else:
            continue
        # print(postinfo.title)


        out_arr.append(
            {
                'uid': postinfo.uid,
                'title': postinfo.title,
                'keywords': postinfo.keywords,
                'date': postinfo.date,
                'extinfo': postinfo.extinfo,
                'cnt_md': postinfo.cnt_md,
                'cnt_html': postinfo.cnt_html,
                'kind': postinfo.kind,
                'user_name': postinfo.user_name,
                'logo': postinfo.logo,
            }
        )

        ff = postinfo.extinfo.get('_tag__file_download')
        if ff :
            pprint(ff)

            # geoinfo = walk_dir(sig)
            # print(sig)
            # print(geoinfo)

        #break

        pp = Path('xx_xml')
        if pp.exists():
            pass
        else:
            pp.mkdir()

        outfile = pp / ( 'drrks-' + postinfo.uid + '.xml')

        fout.write(f'https://drr.ikcest.org/directory/drrks-{postinfo.uid}\n')
        with open(outfile, 'w') as fo:

            fo.write(tmpl_0)
            fo.write('\n')
            fo.write(tp_identifier.format( 'drrks-' + postinfo.uid))
            fo.write('\n')
            fo.write(tp_language.format('English'))
            fo.write('\n')
            # fo.write(tp_subject.format(''))
            fo.write('\n')
            fo.write(tp_title.format(postinfo.title))
            fo.write('\n')
            fo.write(tp_source.format('DRRKS'))
            fo.write('\n')
            # fo.write(tp_relation.format(v5))
            fo.write('\n')
            # markup = postinfo.cnt_html
            # soup = BeautifulSoup(markup)



            fo.write(
                tp_abstract.format(
                    dehtml(
                        tornado.escape.xhtml_unescape(
                        postinfo.cnt_html
                        )
                    )
                    # nltk.clean_html(
                    #     str(
                    #     soup.get_text()
                    #     )
                    # )

                )
            )
            # fo.write(tp_contributor.format(v9))

            fo.write(tmpl_9)



if __name__ == '__main__':
    run_export()
