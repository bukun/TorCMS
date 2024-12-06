
'''
由于启用报地理空间数据库功能，按SpatiaLite设置，或 PostGIS.
'ENGINE':  'django.contrib.gis.db.backends.spatialite',
'ENGINE':  'django.contrib.gis.db.backends.postgis',
'''
DB_INFO =  {
       # 'ENGINE': 'django.db.backends.sqlite3',
       'ENGINE':  'django.contrib.gis.db.backends.spatialite',
       'NAME': 'xx_db.sqlite3',
   }
CACHES_INFO = {}


DEBUG_CFG = True
# DEBUG_CFG = False

