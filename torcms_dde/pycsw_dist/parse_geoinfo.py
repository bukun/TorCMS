from pathlib import Path

import fiona
from osgeo import ogr, osr
from pyproj import CRS, Proj

target = osr.SpatialReference()
target.ImportFromEPSG(4326)

inws = Path('/home/bk/geows')


def get_geo(wdir):
    a, b, c, d = -180, -90, 180, 90
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

        ll = p(ds.bounds[0], ds.bounds[1], inverse=True)
        ur = p(ds.bounds[2], ds.bounds[3], inverse=True)
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
        return a, b, c, d
    else:
        return None

        # print(ext)
        # print(env)


def walk_dir():
    for wdir in inws.rglob('*_dn*'):
        # print('=' * 40)
        # print(wdir)
        uu = get_geo(wdir)

        print(uu)


if __name__ == '__main__':
    walk_dir()
