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

import os
from pathlib import Path
from osgeo import ogr
import fiona
from pyproj import Proj
from pyproj import CRS
from osgeo import osr
import shutil
import subprocess


target = osr.SpatialReference()
target.ImportFromEPSG(4326)

inws = Path('/pb1/drr_datasets')

workdir = Path('/vb1/tmp')

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
    for postinfo in all_recs:
        print('=' * 40)
        # print(postinfo.title)
        sig = postinfo.uid[-4:]


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



    # with open('xx_posts.yaml', "w", encoding='utf-8') as f:
    #     yaml.dump(out_arr, f, allow_unicode=True)



if __name__ == '__main__':
    run_export()
