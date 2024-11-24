import requests  # 导入网页请求模块
import pandas as pd


# 百度米转百度经纬度
def meter2Degree(x, y):
    url = "http://api.map.baidu.com/geoconv/v1/?coords=" + x + "," + y + "&from=6&to=5&output=json&ak=LMIgJaMF56UXqY3xcUpKVSniVXtaPquc"
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'}  # 构造请求头
    response = requests.get(url, headers=header)  # 发出请求
    answer = response.json()  # json化
    result = answer["result"]
    lng = result[0]["x"]
    lat = result[0]["y"]
    return lng, lat


# 提取百度米坐标字符串，转为经纬度坐标串
def coordinateToPoints(coordinates):
    points = ""
    if coordinates and coordinates.index("-") >= 0:
        coordinates = coordinates.split("-")
        temp_coordinates = coordinates[1]
        if temp_coordinates and temp_coordinates.index(",") >= 0:
            temp_coordinates = temp_coordinates.replace(";", "").split(",")
            temp_points = []
            for i in range(0, len(temp_coordinates), 2):
                x = temp_coordinates[i]
                y = temp_coordinates[i + 1]
                point = {}
                point["x"] = x
                point["y"] = y
                temp_points.append(point)
            lng_list = []
            lat_list = []
            for point in temp_points:
                x = point["x"]
                y = point["y"]
                lng, lat = meter2Degree(x, y)
                points += str(lng) + "," + str(lat) + ";\n"
                lng_list.append(lng)
                lat_list.append(lat)
    return points, lng_list, lat_list


# 获取边界
def getBorder(uid):
    # url = "http://map.baidu.com/?pcevaname=pc4.1&qt=ext&ext_ver=new&l=12&uid=" + str(uid)
    url = 'http://map.baidu.com/?pcevaname=pc4.1&qt=ext&ext_ver=new&l=12&uid=' + str(uid)
    # http://map.baidu.com/?reqflag=pcmap&from=webmap&qt=ext&uid=680fb703ea53819c8ab988a9&ext_ver=new&l=18
    # http://map.baidu.com/?reqflag=pcmap&from=webmap&qt=ext&uid=82c5a8f4194f859fede4a513&ext_ver=new&l=18
    # http://map.baidu.com/?pcevaname=pc4.1&qt=ext&ext_ver=new&l=12&uid=82c5a8f4194f859fede4a513
    # http://map.baidu.com/?pcevaname=pc4.1&qt=ext&ext_ver=new&l=12&uid=82c5a8f4194f859fede4a513
    # print(url)
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'}  # 构造请求头
    response = requests.post(url, headers=header)  # 发出请求
    answer = response.json()  # json化
    content = answer["content"]
    points = ""
    lng_list = []
    lat_list = []

    if "geo" in content and content["geo"] != None and content["geo"] != "":
        geo = content["geo"]
        points, lng_list, lat_list = coordinateToPoints(geo)

    return points, lng_list, lat_list


def getlocation(address):


    url = 'https://api.map.baidu.com/geocoding/v3/?address=' + str(
        address) + '&city=长春市&output=json&ak=LMIgJaMF56UXqY3xcUpKVSniVXtaPquc'

    response = requests.post(url)
    # response = requests.get(url=url)
    json_content = response.json()

    if json_content['status'] == 0:
        lng = json_content['result']['location']['lng']  # 经度
        lat = json_content['result']['location']['lat']  # 纬度
        # print(str(lng)+' '+str(lat))
        return lng, lat


def getUid(address, lng, lat):

    url = 'https://api.map.baidu.com/place/v2/search?query=' + str(address) + '&location=' + str(lat) + ',' + str(
        lng) + '&output=json&radius=20&ak=LMIgJaMF56UXqY3xcUpKVSniVXtaPquc'
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'}  # 构造请求头
    response = requests.post(url, headers=header)
    json_content = response.json()
    print("*" * 50)
    print(json_content)
    if json_content['status'] == 0:
        uid = json_content['results'][0]['uid']
        return uid


if __name__ == "__main__":
    # 需要查询的地址
    address = '南关区前进大街102国道'

    # 根据地址获取location (地理编码)
    lng, lat = getlocation(address)
    print(lng,lat)
    # 根据location查找uid （地点检索，圆形区域检索）
    uid = getUid(address, lng, lat)

    # 根据uid查找范围地址边界location
    geo, lng_list, lat_list = getBorder(uid)

    # 写入csv文件中
    df = pd.DataFrame(columns=['经度', '纬度'])
    index = 0
    for i in range(len(lng_list)):
        df.loc[index] = [lng_list[i], lat_list[i]]
        # print(lng_list[i])
        index = index + 1
    df.to_csv(str(address) + '-边界经纬度.csv', mode='a', index=0)