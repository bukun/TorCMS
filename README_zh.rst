TorCMS中文说明
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

引言
===========================

编写目的
----------------------------------

中科东地石山内容管理系统（简称：TorCMS系统）安装部署说明主要用于详细描述整个系统的软硬件组成、系统架构，
以及各组成部分的安装部署方法、配置方法等信息，通过本文档可以对整体系统进行全新部署，或者针对某个组成部分进行重新部署。

TorCMS系统是使用Python 3.4，Tornado Web框架、Peewee、Purecss 开发的，基于Tornado的开源CMS系统。

此CMS系统原本用于云算笔记、开放地理空间实验室等网站，后来慢慢将 CMS 从中抽取出来。
系统运行使用Python 3.4进行开发，经过少量修改，可以运行在 Python 2.7下面，但是发布的版本不对Python 2.7进行特别的支持。
系统默认使用数据库为 SQLite，由于使用了 Peewee，所以可以非常轻松地切换到 MySQL与PostgreSQL。

技术选型
-------------------------------------------------

* 操作系统： Debian
Debian操作系统是使计算机运行的基本程序和工具的集合，其中最主要的部分称为内核 (kernel)。内核是计算机中最重要的程序，负责一切基本的调度工作，并让您运行其他程序。
Debian 系统目前采用 Linux 内核或者 FreeBSD 内核。 Linux 是一个最初由 Linus Torvalds 创建，目前由全球成千上万的程序师共同维护的软件。 FreeBSD 是一个包括内核和其它软件的操作系统。
* 数据库： PostgreSQL
PostgreSQL 是一个自由的对象-关系数据库服务器(数据库管理系统)，它在灵活的 BSD-风格许可证下发行。它提供了相对其他开放源代码数据库系统(比如 MySQL 和 Firebird)，和专有系统(比如 Oracle、Sybase、IBM 的 DB2 和 Microsoft SQL Server)之外的另一种选择。
* 开发语言： Python
Python是纯粹的自由软件，源代码和解释器CPython遵循 GPL(GNU General Public License)协议。
Python的设计目标之一是让代码具备高度的可阅读性。它设计时尽量使用其它语言经常使用的标点符号和英文单字，让代码看起来整洁美观。
* 框架： Tornado
Tornado是python的web框架。Tornado是一种 Web 服务器软件的开源版本。Tornado 和现在的主流 Web 服务器框架（包括大多数 Python 的框架）有着明显的区别：它是非阻塞式服务器，而且速度相当快。
得利于其 非阻塞的方式和对epoll的运用，Tornado 每秒可以处理数以千计的连接，因此 Tornado 是实时 Web 服务的一个理想框架。

系统硬件配置
-------------------------------------

Web与数据库服务器：

* CPU：2核
* 内存：2048 MB
* 操作系统：Debian 8 64位
* 带宽： 1Mbps

运行环境：开发部署于Debian Jessie。但是可在Debian Sqeeze，或其他GNU/Linux发行版运行。数据库使用PostgreSQL 9.5以上版本。
开发语言：Python使用Python 3.4以上版本。

系统应用服务器软件安装与配置
-------------------------------------------------------------------------

系统运行使用Python 3.4进行开发，经过少量修改，可以运行在 Python 2.7下面，但是发布的版本不对Python 2.7进行特别的支持。
系统默认使用数据库为 SQLite，由于使用了 Peewee，所以可以非常轻松地切换到 MySQL与PostgreSQL。
另外，为了使系统正常运行，可能需要安装下面的一些模块：

::

    pip install tornado
    pip install markdown2
    pip install wtforms
    pip install pillow

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
* 最新版本的Jquery 和Bootstrap 作为默认CSS框架

程序部署安装
============================================

Python语言

系统运行支持Python 3.4、Python 3.5、Python 3.6。

获取代码
------------------------------

获取代码:

::

   git clone https://github.com/bukun/TorCMS.git

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


获取HTML模块
--------------------------------------

::

    # cd TorCMS
    git clone https://github.com/bukun/torcms_modules_bootstrap.git templates/modules


编辑configiure
-----------------------------------------------

::

    # cd TorCMS/
    cp cfg_demo.py cfg.py


编辑config.py文件。

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

( DB_CFG 定义用于PostgreSQL项目。）

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

::

* 获取F2E库。
* 初始化PostgreSQL模式。
* 初始化数据库中的元数据
* 初始化whoosh数据库


运行Web程序
---------------------------------------

运行Web应用程序,

::

    python3 server.py 8088

打开Web浏览器输入该地址http://127.0.0.1:8088 即可访问网站主页
(端口在config.py 中定义)

帮助脚本
-----------------------------------

程序中需要使用帮助脚本
运行以下命令以列出不同的脚本：

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

	nosetests3  -v -d --with-coverage tester


API文档的建立
==================================

在 TorCMS文件下

::

	sphinx-apidoc -F -o api_doc torcms

编辑api_doc/conf.py. 添加以下代码后 import os.

::

	sys.path.insert(0, os.path.abspath('../'))

完成以上步骤。然后生成HTML文档。 在TorCMS文件下：

::

	sphinx-build -b html api_doc api_html


功能说明
============================================================
上面介绍了基础的相关操作完成了，可以自己的需求制作项目了。
