TorCMS Introduction
===================

Flexible, extensible web CMS framework built on Tornado and Peewee,
compatible with Python 3.4 and 3.5. Using PostgreSQL with JSON
extension as the database.

pypi: The kernel of this CMS has been submit to pypi.
https://pypi.python.org/pypi/torcms . Could be installed via:

::

    pip install torcms

Application
-----------

-  http://geodata.osgeo.cn/ (The default theme, and DEMO. )

Others
~~~~~~

-  http://www.osgeo.cn
-  http://www.maplet.org
-  http://www.yunsuan.org
-  http://drr.osgeo.cn

Install
=======

Pull the codes.
---------------

::

    git clone https://github.com/bukun/TorCMS.git

Under Debian
------------

::

    aptitude install postgresql-server-dev-all
    aptitude install postgresql-contrib
    aptitude install redis-server

For Python
----------

You should be under Python 3.4 or Python 3.5.

Install libs for Python 3.4 or 3.5,

::

    cd TorCMS/doc
    pip install -r requirements.txt    

How to Run
==========

Pull info\_tags
---------------

Yes, the info\_tags is used to generate database schema and some files needed by every project.

::

    cd TorCMS/src
    git clone https://github.com/bukun/info_tags.git

Edit the configiure.
--------------------

::

    cd TorCMS/src
    copy config_demo.py config.py   

And, edit the config.py file.

Modify the meta information of the web application.
---------------------------------------------------

Modify the file in src/database/meta.

-  doc\_catalog.yaml , which define the catalog of post.
-  info\_tags.xlsx , which define the catalog of info.

Initialize the PostgreSQL schema
--------------------------------

::

    python script_init_table.py

Initialing the metadata in database
-----------------------------------

::

    python script_doc_catalog.py
    python script_info_catalog.py
    cd  info_tags/autocrud
    sh run_gen_all.sh

And, the whoosh database should be initialized first.
-----------------------------------------------------

::

    cd TorCMS/src 
    python script_init_env.py

The upload directory for files should be created.
-------------------------------------------------

::

    mkdir static/upload

Run
---

Do some initializtion work,

::

    python script_init_env.py

Run the web application,

::

    python server.py

Open web brower and navigate to http://127.0.0.1:8088 . 
The port should as be defined in config.py .

Enjoy it!

In Chinese
=========================

本 CMS 是使用Python 3.4，Tornado Web框架， Peewee， Purecss 开发的。
此CMS系统原本用于\ `云算笔记 <http://www.yunsuan.org>`__\ 、\ `开放地理空间实验室 <http://lab.osgeo.cn>`__\ （现合并到\ `OSGeo中国中心 <http://www.osgeo.cn>`__\ ）等网站，
后来慢慢将 CMS 从中抽取出来。

在网站设计方面，提出了文档（Post）、信息（Infor）两种对等的模型进行信息的组织。 这两种模型结构相似，分别用与网站的内容管理，以及应用管理。 其中应用管理，使用了PostgreSQL的JSON扩展，可以设计为App、分类信息、商城应用等。 这些可以在下面的应用中看一下。

网站的文档，除了Post之外，还有Page、Wiki，针对不同的目的作为文档使用。

由于开发者并非计算机专业，对于开发的事情很多只是一知半解，如果有问题，欢迎与我进行联系。
Email: bukun#osgeo.cn

应用
------------------------

-  http://www.osgeo.cn
-  http://www.maplet.org
-  http://www.yunsuan.org
-  http://drr.osgeo.cn

