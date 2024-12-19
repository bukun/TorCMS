import requests
import os
import random
import django
import openpyxl
from pathlib import Path

# file_path = os.path.abspath(os.path.join(os.path.realpath(__file__), '..'))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")
# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")
os.environ["DJANGO_SETTINGS_MODULE"] = "mysite.settings"

django.setup()

from iga.iga_group.models import iga_group
from iga.iga_room.models import iga_room
from iga.iga_floor.models import iga_floor


def chuli_group(group_str):
    group_ids = []
    if group_str:
        if '、' in group_str:
            group_list = group_str.strip().split('、')
            for group in group_list:
                res = iga_group.objects.filter(title=group).first()
                if res:
                    resid = res.id
                else:
                    instance = iga_group.objects.create(title=group)
                    resid = instance.pk
                if resid not in group_ids: group_ids.append(resid)
            # print(group_ids)
        else:
            # print(group_str.strip())
            res = iga_group.objects.filter(title=group_str.strip()).first()
            if res:
                resid = res.id
            else:
                instance = iga_group.objects.create(title=group_str.strip())
                resid = instance.pk
            group_ids = [resid]
    return group_ids


def chuli_room(dic):
    print(dic['room_num'])
    res = iga_room.objects.filter(num=dic['room_num'])
    floorinfo = iga_floor.objects.filter(id=dic['floor']).first()
    group_list = dic['group_ids']
    print(group_list)
    if not res:
        new_info=iga_room.objects.create(
            title=dic['room_title'],
            num=dic['room_num'],
            area=dic['room_area'],
            staff=dic['room_staff'],
            cnt_md=dic['room_cnt'],
            building=dic['room_build'],
            floor=floorinfo,
        )
        update_group(group_list, new_info)

def chuli_floor(num):
    res = iga_floor.objects.filter(num=num).first()

    if res:
        return res.id
    else:
        instance = iga_floor.objects.create(num=num)
        return instance.pk
def update_group(group_list,data):
    for group in group_list:
        if group == '':
            pass
        else:

            c1 = iga_group.objects.filter(id=group).values()

            if c1.first():
                data.group.add(c1.first()['id'])



def start_chuli():
    room_file = Path(__file__).parent / 'xx_20221011.xlsx'
    wb = openpyxl.load_workbook(room_file)
    sheets = wb.sheetnames
    for sheet in sheets:
        # print(sheet)
        if sheet != '封面':
            # print(sheet)
            ws = wb[sheet]
            floor_num = str(sheet).strip()
            floor_id = chuli_floor(sheet)
            # print(floor_id)
            for row in ws.rows:
                sig = row[0].value
                if sig != None and str(sig).strip()[:2] not in ['办公', '房间']:
                    dic = {}
                    dic['room_num'] = str(sig).strip()
                    dic['room_title'] = str(row[1].value).strip()  if row[1] is not None else '无信息'
                    dic['room_group'] = str(row[2].value).strip()
                    dic['room_staff'] = str(row[3].value).strip()  if row[3] is not None else '无人员信息'
                    dic['room_area'] = str(row[4].value).strip() if row[4] is not None else '无面积信息'
                    dic['room_cnt'] = str(row[5].value).strip() if row[5] is not None else '无用途信息'
                    dic['room_build'] = sheet.strip()[:2]

                    # print(dic['room_group'])
                    group_ids = chuli_group(dic['room_group'])

                    dic['group_ids'] = group_ids
                    dic['floor'] = floor_id
                    print(dic)
                    chuli_room(dic)


if __name__ == "__main__":
    start_chuli()
