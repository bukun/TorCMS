import json
import io

"""
这是一个webdog mapeditor3地图编辑器内部数据格式转换为geojson格式的工具
"""


class Webdog:
    """
    weight和dash_array参数用于还原图层样式中的dashArray设置
    因为mapeditor3中，dashArray参数是根据wight进行动态计算的
    所以在存储配置时，只保存了dashArray的类型编号，而不是真正的array
    因此需要进行转换
    """
    WEIGHT = 2
    DASH_ARRAY = {
        1: None,
        2: lambda w: [w * 2],
        3: lambda w: [w * 3, w * 2, 1, w * 2],
        4: lambda w: [w * 4, w * 2, 1, w * 2, 1, w * 2],
        5: {
            'lineCap': 'butt',
            'fn': lambda w: [1]
        },
        6: {
            'lineCap': 'butt',
            'fn': lambda w: [w, w]
        }
    }

    def __init__(self, map_data):
        self.map = None

        if isinstance(map_data, str):
            self.loads(map_data)
        elif isinstance(map_data, dict):
            self.map = map_data
        elif isinstance(map_data, io.IOBase):
            self.load(map_data)

    def _iter_layers(self, key=None):
        if not key:
            key = self.map['begin']

        layer = self.map['layers'][key]

        yield layer

        if 'children' in layer:
            for layer in self._iter_layers(layer['children']):
                yield layer

        if 'next' in layer:
            for layer in self._iter_layers(layer['next']):
                yield layer

    def get_style(self, style):
        if 'dashArray' not in style or style['dashArray'] == 1:
            return style

        dash_array = self.DASH_ARRAY[style['dashArray']]
        weight = style.get('weight') or self.WEIGHT

        if isinstance(dash_array, dict):
            style['dashArray'] = dash_array.fn(weight)
            style['lineCap'] = dash_array['lineCap']
        else:
            style['dashArray'] = dash_array(weight)

        return style

    def is_multi_path(self, coord):
        return isinstance(coord[0][0], list) and isinstance(coord[0][0][0], list)

    def reverse_coord(self, coord):
        if isinstance(coord[0], list):
            for array in coord:
                self.reverse_coord(array)
        else:
            coord.reverse()

        return coord

    def load(self, fp, *args, **kwargs):
        self.map = json.load(fp, *args, **kwargs)
        return self

    def loads(self, s, *args, **kwargs):
        self.map = json.loads(s, *args, **kwargs)
        return self

    def to_geojson(self, dumps=True):
        features = []

        for layer in self._iter_layers():
            layer_type = layer.get('type')

            if not layer_type:
                break

            coord = layer.get('coord')
            name = layer.get('name')
            note = layer.get('note')
            style = layer.get('style')
            properties = layer.get('properties') or {}
            feature_type = None

            if layer_type == "marker":
                if isinstance(coord[0], list):
                    feature_type = 'MultiPoint'
                else:
                    feature_type = 'Point'
            elif layer_type == 'polyline':
                if self.is_multi_path(coord):
                    feature_type = 'MultiLineString'
                else:
                    feature_type = 'LineString'
            elif layer_type == 'polygon':
                if self.is_multi_path(coord):
                    feature_type = 'MultiPolygon'
                else:
                    feature_type = 'Polygon'

            if name:
                properties['name'] = name

            if note:
                properties['note'] = note

            if style:
                properties.update(self.get_style(style))

            feature = {
                'type': 'Feature',
                'properties': properties,
                'geometry': {
                    'type': feature_type,
                    'coordinates': self.reverse_coord(coord)
                }
            }
            features.append(feature)

        geojson = {
            "type": "FeatureCollection",
            "features": features
        }

        if dumps:
            return json.dumps(geojson)
        else:
            return geojson


def webdog_to_geojson(data):
    return Webdog(data).to_geojson()
