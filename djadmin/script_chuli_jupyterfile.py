# 处理上传的jupyter文件，保留code类型cell。并将内容保存到新文件内容，新文件内容命名为jt123.ipynb。
import requests
import os
import random
import django
import nbformat
from pathlib import Path

# file_path = os.path.abspath(os.path.join(os.path.realpath(__file__), '..'))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")
# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")
os.environ["DJANGO_SETTINGS_MODULE"] = "mysite.settings"

django.setup()

from jupyters.jupyter_data.models import Jupyter


def chuli_db():
    for obj in Jupyter.objects.all():
        print('=' * 40)
        print(obj.file_id)
        # file_src = os.path.join(obj.file.path)

        if obj.file_id.startswith('jt') and len(str(obj.file_id)) == 6:
            # file_id = obj.file_id
            pass
        else:
            # 处理已经上传的jupyter信息，但fileid值有问题的地方。
            print(obj.file_id)
            file_id = gen_id()
            while Jupyter.objects.filter(file_id=file_id):
                file_id = gen_id()
            print(file_id)
            obj.file_id = file_id
            obj.save()



def gen_id():
    return 'jt' + ''.join(random.sample(list('0123456789abcdef'), 4))


def chuli_jupyterfile():
    new_jupyter_path = Path(__file__).parent / 'xx_new_jupyter'
    if new_jupyter_path.exists():
        pass
    else:
        new_jupyter_path.mkdir()
    for obj in Jupyter.objects.all():
        print(obj.file_id)
        file_src = os.path.join(obj.file.path)
        print(obj.file.path)
        print(file_src)

        file_id = obj.file_id

        with open(file_src, 'r', encoding='utf-8') as f:
            notebook = nbformat.read(f, as_version=4)
        # print(notebook)
        new_nb = nbformat.v4.new_notebook()

        for cell in notebook.cells:
            if cell.cell_type == 'code':
                new_nb.cells.append(cell)

        file_name = file_id + '.ipynb'
        out_file = new_jupyter_path / file_name
        print(out_file)

        if out_file.exists():
            print('PASS: ', out_file)
            pass
        else:
            with open(out_file, 'w', encoding='utf-8') as f:
                nbformat.write(new_nb, f)
            # out_file.write_bytes(new_nb)


if __name__ == "__main__":
    # chuli_db()
    chuli_jupyterfile()
