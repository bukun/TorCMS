
## PostgreSQL配置环境变量

    export PGPORT=5432
    export PGHOST=localhost 
    export PGUSER=pgis 
    export PGPASSWORD="password" 
    export PGDATABASE=pgis


## PostGIS访问

参考：https://mapserver.org/input/vector/postgis.html


    gdalinfo PG:"host=127.0.0.1 port=5432 user=pgis password=password dbname=pgis"
    gdalinfo PG:"host=127.0.0.1 port=5432 user=pgis password=password dbname=pgis table=ras_f2_night_wind_direction column=rast" -nomd 

## 访问地图与图例

    http://47.104.152.23/cgi-bin/mapserv?MAP=/qsvr/geodata/mfile_weather.map&service=wms&REQUEST=GetLegendGraphic&VERSION=1.0.0&FORMAT=image/png&WIDTH=20&HEIGHT=20&LAYER=lyr_f1_day_air_temperature