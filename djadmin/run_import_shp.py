from pathlib import Path
import world
# world_shp = Path(world.__file__).resolve().parent / "data" / "TM_WORLD_BORDERS-0.3.shp"
world_shp = Path('../assets/TM_WORLD_BORDERS-0.3.shp')
from django.contrib.gis.gdal import DataSource
ds = DataSource(world_shp)
print(ds)
lyr = ds[0]
print(lyr)
print(lyr.geom_type)
print(len(lyr))
srs = lyr.srs
print(srs)
print(srs.proj)
print(lyr.fields)
for feat in lyr:
    print(feat.get("NAME"), feat.geom.num_points)

feat = lyr[234]
print(feat.get("NAME"))

world_mapping = {
    "fips": "FIPS",
    "iso2": "ISO2",
    "iso3": "ISO3",
    "un": "UN",
    "name": "NAME",
    "area": "AREA",
    "pop2005": "POP2005",
    "region": "REGION",
    "subregion": "SUBREGION",
    "lon": "LON",
    "lat": "LAT",
    "mpoly": "MULTIPOLYGON",
}

from django.contrib.gis.utils import LayerMapping
from world.models import WorldBorder

lm = LayerMapping(WorldBorder, world_shp, world_mapping, transform=False)