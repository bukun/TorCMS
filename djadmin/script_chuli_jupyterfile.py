# 处理上传的jupyter文件，保留code类型cell。并将内容保存到新文件内容，新文件内容命名为jt123.ipynb。
import requests
import os
import random
import django
import nbformat
from pathlib import Path
file_path = os.path.abspath(os.path.join(os.path.realpath(__file__), '..'))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")
# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")
os.environ["DJANGO_SETTINGS_MODULE"] = "mysite.settings"
if django.VERSION >= (1, 7):  # 自动判断版本
    django.setup()

from jupyters.jupyter_data.models import Jupyter

django.setup()


def chuli_jupyterfile():
    for obj in Jupyter.objects.all():
        print(obj.file_id)
        file_src = os.path.join(obj.file.path)

        if obj.file_id.startswith('jt') and len(str(obj.file_id))==6:
            file_id = obj.file_id
        else:
            # 处理已经上传的jupyter信息，但fileid值有问题的地方。
            file_id = 'jt' + ''.join(random.sample(list('0123456789abcdefghijklmnopqrstuvwxyz'), 4))
            while Jupyter.objects.filter(file_id=file_id):
                file_id = 'jt' + ''.join(random.sample(list('0123456789abcdefghijklmnopqrstuvwxyz'), 4))
            obj.file_id = file_id
            obj.save()

        with open(file_src, 'r', encoding='utf-8') as f:
            notebook = nbformat.read(f, as_version=4)
        # print(notebook)
        new_nb = nbformat.v4.new_notebook()

        for cell in notebook.cells:
            if cell.cell_type == 'code':
                new_nb.cells.append(cell)

        new_jt_file = file_path + '/xx_new_jupyter'
        file_name =  file_id + '.ipynb'
        if not os.path.exists(new_jt_file):
            os.makedirs(new_jt_file)
        for roo,dirs,files in os.walk(new_jt_file):
            if file_name in files:
                pass
            else:
                with open(new_jt_file + '/' + file_id + '.ipynb', 'w', encoding='utf-8') as f:
                    nbformat.write(new_nb, f)
if __name__ == "__main__":
    chuli()
