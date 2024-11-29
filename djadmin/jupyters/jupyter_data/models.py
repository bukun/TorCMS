import re
import html2text as ht
import os
import re
import subprocess
from pathlib import Path
import bs4
import markdown
from django.db import models
from django.contrib.auth import get_user_model
from base.models import basemodel
from mdeditor.fields import MDTextField
from jupyters.jupyter_category.models import JupyterCatagory
from django.utils.safestring import mark_safe
from django.contrib.sites.models import Site
User = get_user_model()


DC_IMAGE_CHOICES = [
('scipy', 'python 基础'),
('1', 'python 绘图'),
('2', 'R语言'),
]
class Jupyter(basemodel):

    file = models.FileField(upload_to='jupyter/files/', null=True, blank=True, verbose_name="文件")
    dc_image = models.CharField(choices=DC_IMAGE_CHOICES, verbose_name="容器镜像ID",default='scipy',max_length=255)
    category = models.ForeignKey(JupyterCatagory, on_delete=models.CASCADE, blank=True, null=True,
                                 related_name='jupyter_data', verbose_name='分类名称')
    file_id = models.CharField(blank=True, null=False, max_length=255, verbose_name="文件ID")
    title = models.CharField(blank=True, null=False, max_length=255, verbose_name="标题")

    cnt_md = MDTextField(verbose_name="内容", null=True, blank=True)
    logo = models.ImageField(upload_to='jupyter/imgs/', max_length=255, null=True, blank=True,
                             verbose_name="图片")
    shared_with = models.ManyToManyField(User, related_name='shared_with', verbose_name="分享给好友", blank=True)
    sites = models.ManyToManyField(Site,blank=True, related_name='jupyter', verbose_name='Site')


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



        subprocess.run(f'jupyter nbconvert --to html {ch_path.resolve()} --output /tmp/xx.html ', shell=True)

        html_file = '/tmp/xx.html'

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


        self.cnt_md = markdown_content
        self.title = title
        self.file_id = uid
    class Meta(basemodel.Meta):
        db_table = 'jupyter'
        verbose_name = "科学计算模型数据"
        verbose_name_plural = verbose_name
