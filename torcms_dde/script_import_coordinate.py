# -*- coding:utf-8 -*-
import requests
import json
import time
import uuid
import socket
from openpyxl import load_workbook

 
ak = 'UwHxw3gMu9G3zxjC5Ug5SQhoZnSCSIei'
tx='3JLBZ-I2OWJ-3AAFI-KDLGM-UMDPO-Q6BRM'


header_dict = dict()

header_dict['Accept'] = '*/*'
header_dict['Content-Type'] = 'application/json'
header_dict['X-Ca-Signature-Headers'] = 'x-ca-key,x-ca-nonce,x-ca-timestamp'

def get_coor(ip,error_list):
    #  baidu  api (国内 )
    url = 'https://api.map.baidu.com/location/ip?ak={}&ip={}&coor=bd09ll'.format(ak,ip)
    # 免费api（访问可能429状态码）
    url1 = 'http://ip-api.com/json/{}?lang=zh-CN'.format(ip)
    # tx api(请求时间过长,准确度差)
    url2 ='https://apis.map.qq.com/ws/location/v1/ip?ip={}&key={}'.format(ip,tx)
    # print(url)
    time.sleep(2)
    try:
        res = requests.get(url1,headers = header_dict)
    except Exception:
        res = None
        error_list.append({'url:'+url1 + ', ip:' + ip })
        f = 'xx_error_list.json'
        with open(f, 'w') as file_obj:
            json.dump(error_list, file_obj, ensure_ascii=False)
    print(res)
    if res and res.status_code == 200:
        print(ip, res.status_code)
        tojson = json.loads(str(res.content.decode('utf-8')))

        return tojson



def get_url():
    fil = './全球灾害数据库20221208.xlsx'

    # f = 'xx_coor.json'
    # with open(f, 'r') as file_obj:
    #     load_dict = json.load(file_obj)
    #
    # coor_list = load_dict
    # print("*" * 50)
    # print(coor_list)
    coor_list = []
    reapt_list =[]
    error_list =[]
    wb = load_workbook(fil)
    ws = wb['Sheet1']
    i = 0
    for row in ws.rows:
        sig = row[2].value
        if sig != '网址':
            url = row[2].value
            print("*" * 50)
            print(i, url)
            ip = get_ip(url)
            i = i+1
            # print(ip)
            if ip != '':
                dic = get_coor(ip,error_list)
                print(dic)
                try:
                    ip_coor = {
                        'ip': ip,
                        'lat': dic['lat'],
                        'lon': dic['lon'],
                        'place': dic['country'],
                        # 'url':  url
                        'num':1
                    }
                    for x in coor_list:
                        if dic['lat'] == x['lat'] and dic['lon'] == x['lon']:
                            x['num'] = x['num'] + 1
                            ip_coor['num'] = x['num']
                    if ip_coor not in coor_list: coor_list.append(ip_coor)
                    reapt_list.append(sig)

                    f = 'xx_coor.json'
                    with open(f, 'w') as file_obj:
                        json.dump(coor_list, file_obj, ensure_ascii=False)

                except Exception:
                    pass

def get_ip(url):
    no_add = []
    url1 = url.split('://')[1].split('/')[0]
    try:
        myadd = socket.gethostbyname(url1)
    except Exception:
        no_add.append(url)

        myadd=''
        f = 'xx_no_add.json'
        with open(f, 'w') as file_obj:
            json.dump(no_add, file_obj, ensure_ascii=False)
    return myadd
if __name__=='__main__':
    get_url()