import re
import html2text as ht
import os
import re
import subprocess
from pathlib import Path
import bs4
import markdown
import random
from django.db import models
from django.contrib.auth import get_user_model
from base.models import basemodel
from mdeditor.fields import MDTextField
from jupyters.jupyter_category.models import JupyterCatagory
from django.utils.safestring import mark_safe
from django.contrib.sites.models import Site
User = get_user_model()
from django.conf import settings



DC_IMAGE_CHOICES = [
('bio', 'bio'),
]
class Jupyter(basemodel):

    file = models.FileField(upload_to='jupyter/files/', null=True, blank=True, verbose_name="文件")
    dc_image = models.CharField(choices=DC_IMAGE_CHOICES, verbose_name="容器镜像ID",default='bio',max_length=255)
    category = models.ForeignKey(JupyterCatagory, on_delete=models.CASCADE, blank=True, null=True,
                                 related_name='jupyter_data', verbose_name='分类名称')

    file_id = models.CharField(blank=True, null=False, max_length=255, verbose_name="文件ID",unique=True)

    title = models.CharField(blank=True, null=False, max_length=255, verbose_name="标题")

    cnt_md = MDTextField(verbose_name="内容", null=True, blank=True)

    logo = models.ImageField(upload_to='jupyter/imgs/', max_length=255, null=True, blank=True,
                             verbose_name="图片")
    shared_with = models.ManyToManyField(User, related_name='shared_with', verbose_name="分享给好友", blank=True)
    sites = models.ManyToManyField(Site,blank=True, related_name='jupyter', verbose_name='Site')

    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, editable=False,
                             null=True, related_name='jupyter', verbose_name='用户名')


    def __str__(self):
        return self.title
    def get_html_content(self):
        html_content = markdown.markdown(self.cnt_md)
        return mark_safe(html_content)
    def save(self, *args, **kwargs):
        super(Jupyter, self).save(*args, **kwargs)

        if not self.cnt_md:

            self.convert_to_markdown()

            super(Jupyter, self).save(*args, **kwargs)


    def convert_to_markdown(self):

        rest_regs = [
            # '\s:.+?:`.+?`\/:.+?:`.+?`\/:.+?:`.+?`'
            '\<img.+?\/\>',  # 形如：   ``sadf``: :sdf:`slfkj`

        ]

        file_src = os.path.join(self.file.path)
        ch_path = Path(os.path.join(file_src))
        if ch_path.stem.split('_')[-2]:
            uid=ch_path.stem.split('_')[-2]
        else:
            uid = ch_path.stem.split('_')[-1]

        current_directory = os.path.dirname(self.file.path)
        # 获取上一层目录
        parent_directory = os.path.dirname(current_directory)

        html_file = f'{parent_directory}/xx.html'
        subprocess.run(f'jupyter nbconvert --to html {ch_path.resolve()} --output {html_file} ', shell=True)

        # File = open(str(the_file.resolve()))
        Soup = bs4.BeautifulSoup(open(html_file).read(), features="html.parser")


        title = Soup.select('h1')[0].getText()
        content = Soup.select('.jp-Notebook')

        # title.replace('{', '{{').replace('}', '}}')
        # 术语、参考
        phoneNumRegex = re.compile('|'.join(rest_regs))
        # print(in_text)
        in_text = str(content)

        out_reg_arr = phoneNumRegex.findall(in_text)

        if out_reg_arr:
            out_text_arr = phoneNumRegex.split(in_text)
        else:
            out_text_arr = [in_text]
        result = [None] * (len(out_text_arr) + len(out_reg_arr))
        result[::2] = out_text_arr
        result[1::2] = out_reg_arr

        # print(result)

        content = ' '.join(result)[1:-1]
        html_content=str(content).replace('class="container"', '')
        # 将HTML转换为Textile
        text_maker = ht.HTML2Text()
        text_maker.bypass_tables = False
        markdown_content = text_maker.handle(html_content)

        file_id = 'jt' + ''.join(random.sample(list('0123456789abcdefghijklmnopqrstuvwxyz'), 4))
        while Jupyter.objects.filter(file_id=file_id):
            file_id = 'jt' + ''.join(random.sample(list('0123456789abcdefghijklmnopqrstuvwxyz'), 4))

        self.file_id = file_id
        self.cnt_md = markdown_content
        self.title = title
    class Meta(basemodel.Meta):
        db_table = 'jupyter'
        verbose_name = "科学计算模型数据"
        verbose_name_plural = verbose_name
