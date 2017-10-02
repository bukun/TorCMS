TorCMS中文说明
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

引言
===========================

编写目的
----------------------------------

中科东地石山内容管理系统（简称：TorCMS系统）安装部署说明主要用于详细描述整个系统的软硬件组成、系统架构，
以及各组成部分的安装部署方法、配置方法等信息，通过本文档可以对整体系统进行全新部署，或者针对某个组成部分进行重新部署。

TorCMS系统是使用Python 3.4，Tornado Web框架、Peewee、BootStrap开发的，基于Tornado的开源CMS系统。

此CMS系统原本用于云算笔记、开放地理空间实验室等网站，后来慢慢将 CMS 从中抽取出来。
系统运行使用Python 3.4进行开发，经过少量修改，可以运行在 Python 2.7下面，但是发布的版本不对Python 2.7进行特别的支持。
由于使用了 PostgreSQL 的 JSON 扩展功能，系统目前仅支持 PostgreSQL 。

TorCMS系统的功能特征
----------------------------------------------

功能特征如下：

* TorCMS基于Tornado Web框架，该语言简洁清晰。
* 该语言使用Markdown编辑器，便于打造干净清晰的HTML代码
* 精心设计默认模板，如Post, Info, Page, Wiki等。
* 编辑用户角色
* 全文检索
* PostgreSQL 9.4以上，使用JSONB以便于框架可扩展。
* 通过Peewee访问数据库。
* Style的SASS子项目。
* 最新版本的Jquery 和Bootstrap 作为默认JavaScript与CSS框架。

程序部署安装
============================================

Python语言

系统运行支持Python 3.4、Python 3.5、Python 3.6。

在Debian下安装
-------------------------------------

::

    aptitude install postgresql-server-dev-all
    aptitude install postgresql-contrib
    aptitude install redis-server

搭建数据库
-------------------------------------------------------
在PostgreSQL中创建数据库和用户。该信息应该在config.py文件中使用。 并且，在数据库中创建hstore扩展。

首先切换到系统用户：

::

    su - postgres
然后输入：

::
    psql

进入到postgresql环境，
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
    $ git clone https://github.com/bukun/torcms_modules_bootstrap.git templates/modules


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

修改TorCMS/database/meta中的文件

* doc_catalog.yaml , （定义post目录 ）
* info_tags.xlsx , （定义info目录）

初始化
-------------------------------------------------

运行代码：

::

    python3 helper.py -i init

它将：


* 获取F2E库。
* 初始化PostgreSQL模式。
* 初始化数据库中的元数据
* 初始化whoosh数据库


运行Web程序
---------------------------------------

运行Web应用程序,

::

    python3 server.py 8088

打开Web浏览器输入该地址http://127.0.0.1:8088 即可访问网站首页。
(端口在 ``config.py`` 中定义)

帮助脚本
-----------------------------------

程序中需要使用帮助脚本， 运行以下命令以列出不同的脚本：

::

    python3 helper.py -h


运行python3 helper.py -i切换脚本，我们使用的init做一些初始化。

* migrate : 用于数据库模式更改。
* edit_diff : 发送电子邮件针对于修改的post和page页面.
* sitemap : 为post和page页面生成站点地图.
* check_kind : 检查信息的类型是否正确.
* check : 生成模板关系的图片。 例如：

::

    python3 helper.py -i check templates/theme


单元测试
==================================

首先应该用pip安装nose
注解：nose继承自unittest，且比unittest更容易使用。

::

    pip3 install nose

然后运行如下：

::

    nosetests -v -d tester


如果要运行 coverage来查看单元测试覆盖情况，首先要安装coverage (install with: pip3 install coverage )，然后进行:

::

    nosetests3 -v -d --with-coverage tester


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
