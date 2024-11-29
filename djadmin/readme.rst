

问题
==============================

由于启用多站点，在初始化时存在有问题：

::

    django.db.utils.OperationalError: no such table: django_site

解决方法：单独创建， 并创建 ``id`` 为 ``1`` 的一条记录。

如果用 SpatiaLite ，注意安装：

::

    sudo apt install libsqlite3-mod-spatialite

在 SpatiaLite 中如下：

::

    CREATE TABLE "django_site" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "domain" varchar(100) NOT NULL, "name" varchar(50) NOT NULL);
    insert into django_site (id, domain, name) values(1, 'htt', 'hta');

以上处理后，再进行数据迁移时，会出现数据表 **已存在** 的问题。
注意检查出错的文件与行号。
这个得修改脚本，将创建数据库的地方跳过。
如，修改虚拟环境对应文件：

::

    lib/python3.11/site-packages/django/db/backends/sqlite3/base.py

针对出问题函数，修改如下：

::

   def execute(self, query, params=None):
       if params is None:
           if 'CREATE TABLE "django_site"' in query:
               print('=' * 80)
               print(query)
               return None
           return super().execute(query)
或可运行如下命令,此命令是一个在Django框架中执行数据库迁移的命令。这个命令的目的是创建数据库的迁移文件，但是它并不会真正地执行这些迁移，
它只是创建了迁移文件，并将它们标记为已经执行，但实际上并没有改变数据库的结构。

::
    python manage.py migrate --fake-initial



ToDo: 针对 PostGIS，应有所不同，注意处理。

使用 poetry 进行包的管理
========================================

安装 Python Poetry

首先要安装最新版本的 Python Poetry，不要用操作系统自带的。可以先创建虚拟环境，熊岳 使用 pip 命令安装：

::

    pip install poetry

安装完成后，就可以在命令行中使用 poetry 命令了。

Python Poetry 的主要特性

1. 简洁易用的依赖定义

Python Poetry 使用 pyproject.toml 文件来定义项目的依赖和配置信息，这种格式简洁明了，易于理解和维护。通过 pyproject.toml 文件，用户可以轻松地指定项目依赖、Python 版本、项目元数据等信息。

示例代码：

::

    # pyproject.toml

    [tool.poetry]
    name = "myproject"
    version = "0.1.0"
    description = "My Python project"
    authors = ["Your Name <you@example.com>"]

    [tool.poetry.dependencies]
    python = "^3.8"
    requests = "^2.25.1"

    [build-system]
    requires = ["poetry-core>=1.0.0"]
    build-backend = "poetry.core.masonry.api"

2. 虚拟环境管理

Python Poetry 自动为每个项目创建独立的虚拟环境，这样可以确保项目的依赖不会与系统的 Python 环境产生冲突。用户可以在虚拟环境中安装和管理项目的依赖，保持项目的环境隔离性。

示例代码：

::

    poetry init -n


# 创建虚拟环境

::

    poetry env use python3.11

# 激活虚拟环境

::

    poetry shell

可以使用以下命令来添加依赖：

::

    poetry add requests


3. 依赖解析和锁定

Python Poetry 使用锁文件（poetry.lock）来记录项目依赖的精确版本信息，这样可以确保项目在不同环境下的依赖一致性。Poetry 还提供了强大的依赖解析算法，可以有效地解决依赖冲突和版本兼容性问题。

示例代码：

# 安装项目依赖并生成锁文件

::

    poetry install

# 更新依赖并重新生成锁文件

::

    poetry update



Note
=================================


source ~/vpy_django/bin/activate

安装：


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