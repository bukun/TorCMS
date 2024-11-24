source ~/vpy_django/bin/activate

安装：
pip install django

python -m pip install Pillow #上传图片用

pip install djangorestframework #Django REST framework (DRF)是基于Django实现的一个RESTful风格API框架，能够帮助我们快速开发RESTful风格的API，文档地址如下所示:官网：https://www.django-rest-framework.org/

pip install djangorestframework-simplejwt  #JSON Web Token认证后端

pip install django-simpleui

pip install django-import-export #表格批量导入导出功能。

pip install django-cors-headers #后端安装跨域模块

pip install django-cors-headers -i https://pypi.tuna.tsinghua.edu.cn/simple #如果前端与后端的数据来自不同的域名，就会形成跨域问题，只要是协议、域名、端口三者其一不同那就会形成跨域，我们可以使用 CORS 来解决后端对跨域访问的支持

pip install psycopg2-binary

pip install django_redis #缓存

pip install django-ckeditor  #安装ckeditor

pip install django-js-asset #安装js_asset

pip install Scrapy

pip install scrapy_djangoitem

pip install django-mdeditor

pip install html2text
pip install markdown
pip install beautifulsoup4
pip install shapely
pip install django-contrib-comments
pip install geopy #根据经纬度获取城市名称
pip install django-geoposition
pip install djangorestframework-gis
pip install django-bootstrap4
pip install django-friendship
运行：

django-admin startproject mysite  #创建项目

python manage.py startapp demo  #创建新的app

python manage.py flush # 清空数据库(需要时运行)

python manage.py createsuperuser #创建管理员  (admin:Gg01234567)

python manage.py collectstatic #收集静态文件


#以下三条命令在 **sh_helper.sh** 中，每次更改后运行sh_helper.sh即可
python manage.py makemigrations #检查模型有无变化

python manage.py migrate  #将变化迁移至数据表

python manage.py runserver #运行项目

python manage.py inspectdb  # 使用这条命令，会根据设置的数据库中的表在自动生成对应的Model代码，并打印出来

python manage.py inspectdb > student/models.py # 直接将打印的代码直接导入到指定的Model文件中,前提是创建了app(student)并且在setting.py文件中注册过


python manage.py migrate --fake space


**如果关闭debug模式后，请执行以下命令将simpleui静态文件静态文件克隆到根目录**

**python3 manage.py collectstatic**


* 如遇迁移，初始化错误，将各app下migrations中文件删除(保留migrations文件和里面的__init__.py文件)，并将db.sqlite3删除，重新再进行makemigrations,migrate,runserver即可

* 用户建议初始化项目之后再创建，涉及JWT验证加密问题，先创建用户会导致密码错误

**class类访问权限说明**

view.py中更改

* 需登录访问：

继承 `LoginRequiredMixin` `login_url`同时加在类里面

示例：

   `from django.contrib.auth.mixins import PermissionRequiredMixin`

   `class FarmerList(LoginRequiredMixin, generics.ListCreateAPIView):`

        `login_url = '/admin/'`


* 需权限访问：

继承 `PermissionRequiredMixin`

示例：

    `from django.contrib.auth.mixins import PermissionRequiredMixin`

    `class FarmerList(PermissionRequiredMixin, generics.ListCreateAPIView):`

        `login_url = '/admin/'`



**Scrapy**

https://www.runoob.com/w3cnote/scrapy-detail.html

pip install Scrapy

scrapy startproject 项目名      # 创建scrapy项目

scrapy genspider 爬虫名 域名

scrapy crawl 爬虫名

**爬数据**

在当前目录下输入命令，将在mySpider/spider目录下创建一个名为itcast的爬虫，并指定爬取域的范围：

scrapy genspider itcast "itcast.cn"


**保存数据**

scrapy保存信息的最简单的方法主要有四种，-o 输出指定格式的文件，命令如下：

scrapy crawl itcast -o teachers.json

json lines格式，默认为Unicode编码

scrapy crawl itcast -o teachers.jsonl

csv 逗号表达式，可用Excel打开

scrapy crawl itcast -o teachers.csv

xml格式

scrapy crawl itcast -o teachers.xml





**在cmd中创建Scrapy项目工程。**

scrapy startproject mySpider

**解析scrapy框架结构：**

items.py:定义爬虫程序的数据模型

middlewares.py:定义数据模型中的中间件

pipelines.py:管道文件，负责对爬虫返回数据的处理

settings.py:爬虫程序设置，主要是一些优先级设置(将ROBOTSTXT_OBEY=True  改为  False,这行代码表示是否遵循爬虫协议,如果是Ture的可能有些内容无法爬取)

scrapy.cfg:内容为scrapy的基础配置

spiders目录:放置spider代码的目录


**新建main文件执行爬虫代码。**

```
    from scrapy import cmdline
    cmdline.execute("scrapy crawl tutorial".split())
```