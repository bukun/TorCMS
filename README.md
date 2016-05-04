# TorCMS Introduction
Flexible, extensible web CMS framework built on Tornado, Peewee and Purecss, compatible with Python 3.4 and 3.5.

Hoempage:  [http://torcms.yunsuan.org](http://torcms.yunsuan.org)

pypi:  The kernel of this CMS has been submit to pypi.
[https://pypi.python.org/pypi/torcms](https://pypi.python.org/pypi/torcms) . Could be installed via:

    pip install torcms

## Application

* [http://www.maplet.org](http://www.maplet.org)
* [http://www.yunsuan.org](http://www.yunsuan.org)
* [http://www.wetland.ac.cn](http://www.wetland.ac.cn)
* [http://www.osgeo.cn](http://www.osgeo.cn)



# How to Run

## Pull the codes.

    git clone https://github.com/bukun/TorCMS.git

## Edit the configiure.

    cd TorCMS
    copy config_demo.py config.py

And, edit the config.py file.


## Initialize the PostgreSQL schema

    script_init_database_shema.py

## And, the whoosh database should be initialized first.

    python script_build_whoosh_database.py

# The upload directory for files should be created.

    mkdir static/upload

## For Python.

You should be under Python 3.4 or Python 3.5.

Install libs for Python 3.4 or 3.5,

    pip install -r requirements.txt

Do some initializtion work,

    python script_init_whoosh_database

Run the web application,

    python server.py

Open web brower and navigate to http://127.0.0.1:8088 .

Enjoy it!



# In Chinese

本 CMS 是使用Python 3.4，Tornado Web框架， Peewee， Purecss 开发的。
此CMS系统原本用于[云算笔记](http://www.yunsuan.org)、[开放地理空间实验室](http://lab.osgeo.cn)（现合并到[OSGeo中国中心](http://www.osgeo.cn)）等网站，
后来慢慢将 CMS 从中抽取出来。

由于开发者并非计算机专业，对于开发的事情很多只是一知半解，如果有问题，欢迎与我进行联系。 Email: bukun#osgeo.cn

更多的说明，请参见官方网站：  [http://torcms.yunsuan.org/page/about.html](http://torcms.yunsuan.org/page/about.html) 。
