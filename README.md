# TorCMS Introduction
Flexible, extensible web CMS framework built on Tornado and Peewee, compatible with Python 3.4 and 3.5.
Using PostgreSQL with JSON extension as the database.

pypi:  The kernel of this CMS has been submit to pypi.
[https://pypi.python.org/pypi/torcms](https://pypi.python.org/pypi/torcms) . Could be installed via:

    pip install torcms



## Application

### The default theme, and DEMO.
* [http://geodata.osgeo.cn/](http://geodata.osgeo.cn/)  

### Others

* [http://www.osgeo.cn](http://www.osgeo.cn)
* [http://www.maplet.org](http://www.maplet.org)
* [http://www.yunsuan.org](http://www.yunsuan.org)
* [http://drr.osgeo.cn](http://drr.osgeo.cn)

# Install

## Pull the codes.

    git clone https://github.com/bukun/TorCMS.git

## Under Debian

    aptitude install postgresql-server-dev-all
    aptitude install postgresql-contrib
    aptitude install redis-server

## For Python

You should be under Python 3.4 or Python 3.5.

Install libs for Python 3.4 or 3.5,

    cd TorCMS/doc
    pip install -r requirements.txt    

# How to Run

## Pull info_tags

Yes,  the info_tags is used to generate database schema and some files needed by every project.

    cd TorCMS/src
    git clone https://github.com/bukun/info_tags.git

## Edit the configiure file.

    cd TorCMS/src
    copy config_demo.py config.py   

And, edit the config.py file.

    vim config.py

## Modify the meta information of the web application.

Modify the file in src/database/meta.

* doc_catalog.yaml , which defines the catalog for posts.
* info_tags.xlsx , which defines the catalog for infos.

## Initialize the PostgreSQL schema

    python script_init_table.py

## Initialing the database schema

    python script_doc_catalog.py
    python script_info_catalog.py
    cd  info_tags/autocrud
    sh run_gen_all.sh

## And, the whoosh database should be initialized first.

    cd TorCMS/src 
    python script_init_env.py

## The upload directory for files should be created.

    mkdir static/upload

## Run

Do some initializtion work,

    python script_init_env.py

Run the web application,

    python server.py

Open web brower and navigate to http://127.0.0.1:8088 .  The port ('PORT') should  be defined in config.py .

Enjoy it!

# In Chinese

本 CMS 是使用Python 3.4，Tornado Web框架， Peewee开发的，兼容Python 3.5。

此CMS系统原本用于[云算笔记](http://www.yunsuan.org)
、[开放地理空间实验室](http://lab.osgeo.cn)（现合并到[OSGeo中国中心](http://www.osgeo.cn)）等网站，
后来慢慢将 CMS 从中抽取出来。
# 应用

* [OSGeo中国中心](http://www.osgeo.cn)
* [地图云集Maplet](http://www.maplet.org)
* [云算笔记](http://www.yunsuan.org)
* [IKCEST防灾减灾知识服务中心](http://drr.osgeo.cn)

# 注意
由于开发者并非计算机专业，对于开发的事情很多只是一知半解，如果有问题，欢迎与我进行联系。 Email: bukun#osgeo.cn

