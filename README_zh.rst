========================================
TorCMS中文说明
========================================

TorCMS系统是使用Python 3.7，Tornado Web框架、Peewee、BootStrap开发的，
基于Tornado的开源CMS系统。

此CMS系统原本用于云算笔记、开放地理空间实验室等网站，后来慢慢将 CMS 从中抽取出来。
系统运行使用Python 3.7 （原版本基于 Python 3.4 ）进行开发，
经过少量修改，可以运行在 Python 2.7下面，但是发布的版本不对Python 2.7进行特别的支持。
由于使用了 PostgreSQL 的 JSON 扩展功能，系统目前仅支持 PostgreSQL 。

在网站设计方面，提出了文档（Post）、信息（Infor）两种对等的模型进行信息的组织。
这两种模型结构相似，分别用与网站的内容管理，以及应用管理。
其中应用管理，使用了PostgreSQL的JSON扩展，可以设计为App、分类信息、商城应用等。
这些可以在下面的应用中看一下。

网站的文档，除了Post之外，还有Page、Wiki，针对不同的目的作为文档使用。

引言
===========================


TorCMS系统的功能特征
----------------------------------------------

功能特征如下：

* TorCMS基于Tornado Web框架，该语言简洁清晰。
* 该语言使用Markdown编辑器，便于打造干净清晰的HTML代码。
* 精心设计默认模板，如Post, Info, Page, Wiki等。
* 用户权限管理。
* 基于 Python 的内置全文检索。
* PostgreSQL 11 以上，使用JSONB以便于框架可扩展。
* 通过Peewee访问数据库。
* 样式使用SASS子项目进行管理。
* 最新版本的Jquery 和Bootstrap 作为默认JavaScript与CSS框架。

基本设计思路
---------------------------------------------------------
* 内容都按二级分类目录来组织
* 目录浏览有三种方式，对应的查看页面，也有三种方式：
    * `list` ： 最普通的列出；在其中查看页面为 `post` 。
    * `catalog` ： 目录浏览，列出的条目是有前后顺序的；在其中查看页面为 `leaf` 。
    * `filter` ： 可以使用关键词进行过滤；在其中查看页面为 `info` 。

程序部署安装
============================================

Python语言

系统运行支持Python 3.7、Python 3.8。

在Debian下安装
-------------------------------------

::

    apt install -y postgresql postgresql-contrib redis-server

搭建数据库
-------------------------------------------------------
在PostgreSQL中创建数据库和用户。该信息应该在 ``cfg.py`` 文件中使用。 并且，在数据库中创建 hstore 扩展。

首先切换到系统用户：

::

    su - postgres

然后输入：

::

    psql

进入到 postgresql 环境，
接下来开始创建数据库，以下代码一句一句执行:

::

    CREATE USER torcms WITH PASSWORD '111111';
    CREATE DATABASE torcms OWNER torcms;
    GRANT ALL PRIVILEGES ON DATABASE torcms to torcms;
    \c torcms
    create extension hstore;

创建成功，``\q``  退出。

获取代码
------------------------------

获取代码:

::

   git clone https://github.com/bukun/TorCMS.git

获取HTML模块
--------------------------------------

::

    $ cd TorCMS
    $ git clone https://gitee.com/bukun/torcms_f2elib.git static/f2elib


编辑configiure
-----------------------------------------------

::

    $ cd TorCMS
    $ cp cfg_demo.py cfg.py


编辑 ``cfg.py`` 文件。

::

    DB_CFG = {
        'db': 'torcms',
        'user': 'torcms',
        'pass': '111111',
    }

    SMTP_CFG = {
        'name': 'TorCMS',
        'host': "smtp.ym.163.com",
        'user': "admin@yunsuan.org",
        'pass': "",
        'postfix': 'yunsuan.org',
    }

    SITE_CFG = {
        'site_url': 'http://127.0.0.1:8888',
        'cookie_secret': '123456',
        'DEBUG': False
    }

Web应用程序的元数据信息处理
-------------------------------------------------

修改 ``TorCMS/database/meta`` 中的文件

* ``doc_catalog.yaml`` , （定义post 分类，非必需文件，可在 XLSX 中定义 ）
* ``info_tags.xlsx`` , （定义info 分类）

初始化
-------------------------------------------------

运行代码：

::

    python3 helper.py -i init

它将：


* 初始化PostgreSQL模式
* 初始化数据库中的元数据
* 初始化whoosh数据库


运行Web程序
---------------------------------------

运行Web应用程序,

::

    python3 server.py 8088

打开Web浏览器输入该地址 http://127.0.0.1:8088 即可访问网站首页。
(端口在 ``config.py`` 中定义)

帮助脚本
-----------------------------------

程序中需要使用帮助脚本， 运行以下命令以列出不同的脚本：

::

    python3 helper.py -h


运行 ``python3 helper.py -i`` 切换脚本，我们使用的init做一些初始化。

* ``migrate`` : 用于数据库模式更改。
* ``edit_diff`` : 发送电子邮件针对于修改的post和page页面.
* ``sitemap`` : 为post和page页面生成站点地图.
* ``check_kind`` : 检查信息的类型是否正确.
* ``check`` : 生成模板关系的图片。 例如：

::

    python3 helper.py -i check templates/theme


单元测试
==================================

首先应该用 pip 安装 pytest 。


::

    pip3 install pytest

然后运行如下：

::

    python3 -m pytest tester


API文档的建立
==================================

在 TorCMS文件下

::

    sphinx-apidoc -F -o api_doc torcms

编辑 ``api_doc/conf.py`` 。 添加以下代码后 ``import os`` .

::

    sys.path.insert(0, os.path.abspath('../'))

完成以上步骤。然后生成HTML文档。 在TorCMS文件下：

::

    sphinx-build -b html api_doc api_html


功能说明
============================================================
上面介绍了基础的相关操作完成了，可以自己的需求制作项目了。



关于 `tornado_wtforms` 的说明
======================================

`tornado_wtforms` 是一个基于 `tornado` 和 `wtforms` 的表单验证库，
它提供了 `tornado` 的 `RequestHandler` 的 `form` 属性，用于处理表单验证。

`tornado_wtforms` 是从 `wtforms_tornado` 项目fork而来，它修复了 `wtforms_tornado` 的一些bug，
同时添加了一些新的功能。
但是在 pypi 上的 `tornado_wtforms` 项目自2022年发布后，就再也没有更新过。

在项目使用中，直接将 `tornado_wtforms` 项目中的 `tornado_wtforms` 文件夹（模块）复制到项目中，
然后使用 `from torcms.tornado_wtforms.form import Form` 即可。
