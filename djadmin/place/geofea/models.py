import exifread
from django.db import models
from django.contrib.auth import get_user_model
from base.models import basemodel
from mdeditor.fields import MDTextField
from django.contrib.gis.db import models as gismodels
from django.contrib.gis.geos import Point
from mdeditor.fields import MDTextField
from mptt.models import MPTTModel, TreeForeignKey

User = get_user_model()


class Geofea(basemodel):
    title = models.CharField(blank=True, null=False, max_length=255, verbose_name="标题")
    cnt_md = MDTextField(verbose_name="内容", null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, editable=False,
                             null=True, related_name='geofea', verbose_name='用户名', )
    status = models.BooleanField(blank=False, null=True, verbose_name="是否发布", default=0)

    def __str__(self):
        return self.title

    class Meta(basemodel.Meta):
        db_table = 'geofeaq'
        verbose_name = "Geofea"
        verbose_name_plural = verbose_name


class GeoPage(basemodel):
    title = models.CharField(blank=True, null=False, unique=True, max_length=255, verbose_name="标题")
    txt = MDTextField(verbose_name="内容", null=True, blank=True)
    extinfo = models.JSONField(null=True, default=dict, verbose_name='Extra data in JSON.', blank=True)

    # 判断指定字段长度,超出部分用省略号代替
    def update_content(self):
        if len(str(self.txt)) > 150:
            return '{}...'.format(str(self.txt)[0:150])
        else:
            return self.txt

    # 字段数据处理后,字段verbose_name参数失效
    # 需要重新指定,否则列表页字段名显示的是方法名(update_content)
    update_content.short_description = '内容'

    def __str__(self):
        return self.txt

    class Meta(basemodel.Meta):
        db_table = 'geopage'
        verbose_name = "地名页面"
        verbose_name_plural = verbose_name


class statetype(models.IntegerChoices):
    type1 = 0, '国内'
    type2 = 1, '国外'


class LinearFeatures(basemodel):
    '''
    线状要素库
    '''
    region = models.CharField(max_length=255, blank=True, null=True, verbose_name="所属地区")
    location_name = models.CharField(max_length=255, blank=True, null=True, verbose_name="现代地名")
    historical_name = models.CharField(max_length=255, blank=True, null=True, verbose_name="历史地名")
    set_time = models.CharField(max_length=255, blank=True, null=True, verbose_name="设置时间")
    cancel_time = models.CharField(max_length=255, blank=True, null=True, verbose_name="取消时间")
    lat = models.CharField(blank=True, null=True, default=0, max_length=255, verbose_name="纬度")
    lon = models.CharField(blank=True, null=True, default=1, max_length=255, verbose_name="经度")
    zoom = models.FloatField(blank=True, null=True, default=8, verbose_name="缩放级别")
    content = MDTextField(verbose_name="介绍", null=True, blank=True)
    location = gismodels.LineStringField(null=True, blank=True, verbose_name="位置")
    is_en = models.IntegerField(choices=statetype.choices, verbose_name="国内外", default=0)

    def __str__(self):
        return str(self.id)

    def to_dict(self):
        return {
            'id': self.id,
            'region': self.region,
            'location_name': self.location_name,
            'historical_name': self.historical_name,
            'set_time': self.set_time,
            'cancel_time': self.cancel_time,
            'lat': self.lat,
            'lon': self.lon,
            'zoom': self.zoom,
            'content': self.content,
            'is_en': self.is_en
        }

    class Meta(basemodel.Meta):
        db_table = 'linearfeatures'
        verbose_name = "线状要素库"
        verbose_name_plural = verbose_name


class Photoinfo(basemodel):
    title = models.CharField(blank=True, null=False, max_length=255, verbose_name="标题")
    logo = models.ImageField(upload_to='photo_info/imgs/', max_length=255, null=True, blank=True,
                             verbose_name="图片")
    lat = models.CharField(blank=True, null=True, default=0, max_length=255, verbose_name="纬度")
    lon = models.CharField(blank=True, null=True, default=1, max_length=255, verbose_name="经度")
    cnt_md = MDTextField(verbose_name="内容", null=True, blank=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        super(Photoinfo, self).save(*args, **kwargs)
        if self.logo:
            self.convert_to_photo()
            super(Photoinfo, self).save(*args, **kwargs)

    def convert_to_photo(self):
        file_src = os.path.join(self.logo.path)
        x, y = self.get_single_gps(file_src)
        self.lat = y
        self.lon = x
        # print(x,y)

    def get_single_gps(self, img):
        with open(str(img), 'rb') as f:
            # 直接读取度分秒格式的经纬度数据
            contents = exifread.process_file(f)
            try:
                longitude = contents["GPS GPSLongitude"].values
                has_longitude = True
            except:
                has_longitude = False
            if not has_longitude:
                return '', ''
            else:
                longitude = contents["GPS GPSLongitude"].values
                latitude = contents["GPS GPSLatitude"].values
                # 度分秒转换成十进制数据
                longitude_f = longitude[0].num / longitude[0].den + (longitude[1].num / longitude[1].den / 60) + (
                        longitude[2].num / longitude[2].den / 3600)
                latitude_f = latitude[0].num / latitude[0].den + (latitude[1].num / latitude[1].den / 60) + (
                        latitude[2].num / latitude[2].den / 3600)
                return longitude_f, latitude_f

    class Meta(basemodel.Meta):
        db_table = 'photoinfo'
        verbose_name = "Photoinfo"
        verbose_name_plural = verbose_name


class PlaceName(basemodel):
    '''
    地名库设计为县、乡及以上行政单元的存储库。
    侧重于古代地名的整编。
    数据库的设计包含有“历史地名”，“经度”，“纬度”，“设置时间”，“取消时间”，“现代地名”，“介绍”
    '''
    region = models.CharField(max_length=255, blank=True, null=True, verbose_name="所属地区")
    location_name = models.CharField(max_length=255, blank=True, null=True, verbose_name="现代地名")
    historical_name = models.CharField(max_length=255, blank=True, null=True, verbose_name="历史地名")
    set_time = models.CharField(max_length=255, blank=True, null=True, verbose_name="设置时间")
    cancel_time = models.CharField(max_length=255, blank=True, null=True, verbose_name="取消时间")
    lat = models.CharField(blank=True, null=True, default=0, max_length=255, verbose_name="纬度")
    lon = models.CharField(blank=True, null=True, default=1, max_length=255, verbose_name="经度")
    zoom = models.FloatField(blank=True, null=True, default=8, verbose_name="缩放级别")
    content = MDTextField(verbose_name="介绍", null=True, blank=True)
    location = gismodels.PointField(null=True, blank=True, verbose_name="位置", default=(Point(0, 0, srid=4326)))
    is_en = models.IntegerField(choices=statetype.choices, verbose_name="国内外", default=0)

    def __str__(self):
        return str(self.id)

    def to_dict(self):
        return {
            'id': self.id,
            'region': self.region,
            'location_name': self.location_name,
            'historical_name': self.historical_name,
            'set_time': self.set_time,
            'cancel_time': self.cancel_time,
            'lat': self.lat,
            'lon': self.lon,
            'zoom': self.zoom,
            'content': self.content,
            'is_en': self.is_en
        }

    class Meta(basemodel.Meta):
        db_table = 'place_name'
        verbose_name = "地名库"
        verbose_name_plural = verbose_name


class PlanarFeatures(basemodel):
    '''
    面状要素库
    '''
    region = models.CharField(max_length=255, blank=True, null=True, verbose_name="所属地区")
    location_name = models.CharField(max_length=255, blank=True, null=True, verbose_name="现代地名")
    historical_name = models.CharField(max_length=255, blank=True, null=True, verbose_name="历史地名")
    set_time = models.CharField(max_length=255, blank=True, null=True, verbose_name="设置时间")
    cancel_time = models.CharField(max_length=255, blank=True, null=True, verbose_name="取消时间")
    zoom = models.FloatField(blank=True, null=True, default=8, verbose_name="缩放级别")
    content = MDTextField(verbose_name="介绍", null=True, blank=True)
    location = gismodels.PolygonField(null=True, blank=True, verbose_name="位置")
    is_en = models.IntegerField(choices=statetype.choices, verbose_name="国内外", default=0)

    def __str__(self):
        return str(self.id)

    def to_dict(self):
        return {
            'id': self.id,
            'region': self.region,
            'location_name': self.location_name,
            'historical_name': self.historical_name,
            'set_time': self.set_time,
            'cancel_time': self.cancel_time,
            'zoom': self.zoom,
            'content': self.content,
            'is_en': self.is_en
        }

    class Meta(basemodel.Meta):
        db_table = 'planarfeatures'
        verbose_name = "面状要素库"
        verbose_name_plural = verbose_name


class TestText(basemodel):
    icon = models.CharField(blank=True, unique=True, null=False, max_length=255, verbose_name="图标")
    txt = MDTextField(verbose_name="内容", null=True, blank=True)

    def update_content(self):
        if len(str(self.txt)) > 150:
            return '{}...'.format(str(self.txt)[0:150])
        else:
            return self.txt

    # 字段数据处理后,字段verbose_name参数失效
    # 需要重新指定,否则列表页字段名显示的是方法名(update_content)
    update_content.short_description = '内容'

    def __str__(self):
        return self.txt

    class Meta(basemodel.Meta):
        db_table = 'testtext'
        verbose_name = "测试文本"
        verbose_name_plural = verbose_name


class ThematicMaps(basemodel):
    layer = models.CharField(blank=True, null=False, max_length=255, verbose_name="图层")
    label = models.CharField(blank=True, null=False, max_length=255, verbose_name="标签")
    icon = models.CharField(blank=True, null=False, max_length=255, verbose_name="图标")

    def __str__(self):
        return self.layer

    class Meta(basemodel.Meta):
        db_table = 'thematicmaps'
        verbose_name = "专题地图"
        verbose_name_plural = verbose_name


class XZQH(MPTTModel, basemodel):
    '''
    行政区划
    '''

    zoning = models.CharField(max_length=255, unique=True, blank=True, null=False, verbose_name="行政区划代码")
    name = models.CharField(max_length=255, blank=True, null=False, verbose_name="名称")
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children',
                            verbose_name='上级名称')
    content = MDTextField(verbose_name="介绍", null=True, blank=True)

    def __str__(self):
        return str(self.name)

    class Meta(basemodel.Meta):
        db_table = 'xzqh'
        verbose_name = "行政区划"
        verbose_name_plural = verbose_name
