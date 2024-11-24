'''
导入农业气象站数据 1小时采集一次
'''

import os
import json
import requests
import django
from datetime import datetime

header_dict = dict()
header_dict['Accept'] = '*/*'
header_dict['Content-Type'] = 'application/x-www-form-urlencoded'
header_dict['X-Ca-Signature-Headers'] = 'x-ca-key,x-ca-nonce,x-ca-timestamp'
header_dict['version'] = '1.0.0'

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")
if django.VERSION >= (1, 7):  # 自动判断版本
    django.setup()


def import_data():
    from heitu_barn.device_soilmoisture.models import Devicesoilmoisture
    from heitu_barn.device_meteorology.models import Meteorology
    from heitu_barn.device_soilfiveparameters.models import Soilfivepara1
    from heitu_barn.device_soilfiveparametersv2.models import Soilfiveparav2
    from users.models import myuser
    the_dics = {'89860407112270033143': Devicesoilmoisture,
                '89860407112270033136': Meteorology,
                '89860407112270033135': Soilfivepara1,
                '89860407112270033134': Soilfiveparav2,

                }

    url = 'http://nystfw.cn/index.php?act=getlastdata'

    data_list = [{'typenum': '89860407112270033143'  # qingm05401
               },
        {'typenum': '89860407112270033136'  # qingm053

        }, {'typenum': '89860407112270033135'  # qingm052

        }
        , {'typenum': '89860407112270033134'  # qingm051
                 }
    ]
    for data in data_list:
        print(the_dics[data.get('typenum')])
        r = requests.post(url, headers=header_dict, data=data)

        if r.status_code == 200:
            string_data = r.content.decode('utf-8-sig')
            tojson = json.loads(string_data)
            time_format = "%Y-%m-%d %H:%M:%S"
            # 将时间字符串转换为datetime对象
            datetime_obj = datetime.strptime(tojson['time'], time_format)
            # 将datetime对象转换为时间戳
            timestamp = int(datetime_obj.timestamp())
            if data.get('typenum')=='89860407112270033143':
                res = Devicesoilmoisture.objects.filter(devid=tojson.get('sitenumber'), par_datetime=tojson.get('time'))
                print(res)
                if res:
                    print('已存在')
                else:
                    Devicesoilmoisture.objects.create(
                        devid=tojson.get('sitenumber'),
                        typenum=data.get('typenum'),
                        par_timestamp=timestamp,
                        par_datetime=tojson.get('time'),

                        soiltemperature1=tojson['data'].get('土壤温度1(℃)','0'),
                        soiltemperature2=tojson['data'].get('土壤温度2(℃)','0'),
                        soiltemperature3=tojson['data'].get('土壤温度3(℃)','0'),
                        soiltemperature4=tojson['data'].get('土壤温度4(℃)','0'),
                        soiltemperature5=tojson['data'].get('土壤温度5(℃)','0'),
                        soiltemperature6=tojson['data'].get('土壤温度6(℃)','0'),
                        soiltemperature7=tojson['data'].get('土壤温度7(℃)','0'),
                        soiltemperature8=tojson['data'].get('土壤温度8(℃)','0'),
                        soiltemperature9=tojson['data'].get('土壤温度9(℃)','0'),
                        soiltemperature10=tojson['data'].get('土壤温度10(℃)','0'),
                        soiltemperature11=tojson['data'].get('土壤温度11(℃)','0'),
                        soiltemperature12=tojson['data'].get('土壤温度12(℃)','0'),
                        soiltemperature13=tojson['data'].get('土壤温度13(℃)','0'),
                        soiltemperature14=tojson['data'].get('土壤温度14(℃)','0'),

                        soilmoisture1=tojson['data'].get('土壤湿度1(%)','0'),
                        soilmoisture2=tojson['data'].get('土壤湿度2(%)','0'),
                        soilmoisture3=tojson['data'].get('土壤湿度3(%)','0'),
                        soilmoisture4=tojson['data'].get('土壤湿度4(%)','0'),
                        soilmoisture5=tojson['data'].get('土壤湿度5(%)','0'),
                        soilmoisture6=tojson['data'].get('土壤湿度6(%)','0'),
                        soilmoisture7=tojson['data'].get('土壤湿度7(%)','0'),
                        soilmoisture8=tojson['data'].get('土壤湿度8(%)','0'),
                        soilmoisture9=tojson['data'].get('土壤湿度9(%)','0'),
                        soilmoisture10=tojson['data'].get('土壤湿度10(%)','0'),
                        soilmoisture11=tojson['data'].get('土壤湿度11(%)','0'),
                        soilmoisture12=tojson['data'].get('土壤湿度12(%)','0'),
                        soilmoisture13=tojson['data'].get('土壤湿度13(%)','0'),
                        soilmoisture14=tojson['data'].get('土壤湿度14(%)','0'),

                        soilsalinity1=tojson['data'].get('土壤盐分1(mS)','0'),
                        soilsalinity2=tojson['data'].get('土壤盐分2(mS)','0'),
                        soilsalinity3=tojson['data'].get('土壤盐分3(mS)','0'),
                        soilsalinity4=tojson['data'].get('土壤盐分4(mS)','0'),
                        soilsalinity5=tojson['data'].get('土壤盐分5(mS)','0'),
                        soilsalinity6=tojson['data'].get('土壤盐分6(mS)','0'),
                        soilsalinity7=tojson['data'].get('土壤盐分7(mS)','0'),
                        soilsalinity8=tojson['data'].get('土壤盐分8(mS)','0'),
                        soilsalinity9=tojson['data'].get('土壤盐分9(mS)','0'),
                        soilsalinity10=tojson['data'].get('土壤盐分10(mS)','0'),
                        soilsalinity11=tojson['data'].get('土壤盐分11(mS)','0'),
                        soilsalinity12=tojson['data'].get('土壤盐分12(mS)','0'),
                        soilsalinity13=tojson['data'].get('土壤盐分13(mS)','0'),
                        soilsalinity14=tojson['data'].get('土壤盐分14(mS)','0'),

                        dlnum=tojson['data'].get('DL','0'),
                    )
            elif data.get('typenum')=='89860407112270033136':
                res = Soilfivepara1.objects.filter(devid=tojson.get('sitenumber'), par_datetime=tojson.get('time'))
                print(res)
                if res:
                    print('已存在')
                else:
                    Soilfivepara1.objects.create(
                        devid=tojson.get('sitenumber'),
                        typenum=data.get('typenum'),
                        par_timestamp=timestamp,
                        par_datetime=tojson.get('time'),
                        soiltemperature=tojson.get('土壤温度(℃)','0'),
                        soilmoisture=tojson.get('土壤湿度(%)','0'),
                        soilsalinity=tojson.get('土壤盐分(mS/cm)','0'),
                        conductivity=tojson.get('电导率(mS/cm)','0'),
                        phnum=tojson.get('PH','0'),

                        dlnum=tojson['data'].get('DL','0'),
                    )
            elif data.get('typenum')=='89860407112270033135':
                res = Soilfiveparav2.objects.filter(devid=tojson.get('sitenumber'), par_datetime=tojson.get('time'))
                print(res)
                if res:
                    print('已存在')
                else:
                    Soilfiveparav2.objects.create(
                        devid=tojson.get('sitenumber'),
                        typenum=data.get('typenum'),
                        par_timestamp=timestamp,
                        par_datetime=tojson.get('time'),
                        soiltemperature=tojson.get('土壤温度(℃)','0'),
                        soilmoisture=tojson.get('土壤湿度(%)','0'),
                        soilsalinity=tojson.get('土壤盐分(mS/cm)','0'),
                        conductivity=tojson.get('电导率(mS/cm)','0'),
                        phnum=tojson.get('PH','0'),

                        dlnum=tojson['data'].get('DL','0'),
                    )
            elif data.get('typenum')=='89860407112270033134':
                res = Meteorology.objects.filter(devid=tojson.get('sitenumber'), par_datetime=tojson.get('time'))
                print(res)
                if res:
                    print('已存在')
                else:
                    Meteorology.objects.create(
                        devid=tojson.get('sitenumber'),
                        typenum=data.get('typenum'),
                        par_timestamp=timestamp,
                        par_datetime=tojson.get('time'),

                        windspeed=tojson.get('风速(m/s)','0'),
                        winddirection=tojson.get('风向','0'),
                        airtemperature=tojson.get('空气温度(℃)','0'),
                        airhumidity=tojson.get('空气湿度(%)','0'),
                        atmos=tojson.get('大气压力(kPa)','0'),
                        radiation=tojson.get('总辐射（W/m2）','0'),
                        rainfall=tojson.get('降雨量(mm)','0'),
                        photosynthesis=tojson.get('光合有效1(umol* m2*s)','0'),
                        watersurface=tojson.get('水面蒸发(mm)','0'),

                        dlnum=tojson['data'].get('DL','0'),
                    )

if __name__ == '__main__':
    import_data()
