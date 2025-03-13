==============================
TorCMS Introduction
==============================

Status
==============================

.. image:: https://img.shields.io/pypi/v/torcms.svg
    :target: https://pypi.python.org/pypi/torcms/

.. image:: https://img.shields.io/pypi/pyversions/torcms.svg
    :target: https://pypi.python.org/pypi/torcms/

Checking ``torcms`` with ``pylint`` using default configuration (Under Debian 11.0),
gets score greater than 8.9.

Introduction
==============================

Flexible, extensible web CMS framework built on Tornado and Peewee,
compatible with Python 3.7 and above. Using PostgreSQL with JSON
extension as the database( postgresql-server >= 11.0 ).

In 2025, TorCMS had been integrated with Django for backend administration.

pypi: TorCMS has been submit to pypi.
https://pypi.python.org/pypi/torcms . Could be installed via:

::

    pip3 install torcms

Features
==============================

- Build on Tornado, only with Web features, which made it is simple to use.
- Integrated with Django for backend administration.
- Markdown editor, make your HTML clean and clear.
- Carefull desinged model for conents. Post, Info, Page, Wiki as default.
- User roles for editing.
- Full text search with Whoosh.
- PostgreSQL 9.4 above, with JSONB, which makes the framework extensible.
- Using XLXS, could be parsed by ``openpyxl``, to define the schema of the database.
- Access database via Peewee.
- SASS sub-project for Style.
- Last version of JQuery. And, Bootstrap as the default CSS framework.

Application
==============================

-  https://www.osgeo.cn (OSGeo China Chapter)
-  https://ikcest-drr.data.ac.cn/ (Disaster Risk Reduction Knowledge Service of UNESCO)
-  http://wdcrre.data.ac.cn/ (World data center for Renewable Resources and Environment)

-  http://www.maphub.cn (Merged into https://www.osgeo.cn)
-  http://www.yunsuan.org (Merged into https://www.osgeo.cn)


Install
================

Pull the codes.
----------------------

::

    git clone https://github.com/bukun/TorCMS.git

Requirement for the System
---------------------------------------------

Under Debian/Ubuntu
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

::

    $ sudo apt install -y postgresql postgresql-contrib redis-server


Create the Database
---------------------------

Create the database, and user in PostgreSQL.
The information should be used in the ``cfg.py`` file.
And, create hstore extension in the database.

::

    \set dbname torcms
    CREATE USER :dbname WITH PASSWORD '111111' ;
    CREATE DATABASE :dbname OWNER :dbname ;
    GRANT ALL PRIVILEGES ON DATABASE :dbname to :dbname ;
    \c :dbname ;
    create extension hstore;
    \q

For Python
----------

You should be under Python 3.4 or Python 3.5.

Install libs for Python 3.4 or 3.5,

::

    cd TorCMS
    pip3 install -r doc/requirements.txt


For Deiban/Ubutnu
---------------------------------------

If you are to use Python of OS system directly, install libs as:

::

    sudo apt isntall -y python3-tornado python3-requests python3-openpyxl python3-markdown

How to Run
=========================

Get the HTML for modules
----------------------------------

::

    $ cd TorCMS
    $ git clone --depth=1 https://github.com/bukun/torcms_f2elib.git static/f2elib


or using the same f2elib via Gitee:

::

    $ git clone --depth=1 https://gitee.com/bukun/torcms_f2elib.git static/f2elib

Edit the configiure.
-----------------------

::

    $ cd TorCMS/
    $ cp cfg_demo.py cfg.py

And, edit the ``cfg.py`` file.

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

The ``DB_CFG`` defines the items used for PostgreSQL.

Modify the meta information of the web application.
---------------------------------------------------------

Modify the file in ``TorCMS/database/meta``.

-  ``doc_catalog.yaml`` , which define the catalog of post.
-  ``info_tags.xlsx`` , which define the catalog of info.


Initialization
--------------------------------

::

    python3 helper.py -i init

it will

- initialize the PostgreSQL schema.
- initialize the metadata in database.
- the whoosh database would be initialized.


Run
---------


Run the web application,

::

    python3 server.py 8088

Open web brower and navigate to http://127.0.0.1:8088 .

The port should as be defined in config.py .

Enjoy it!

Helper Script
=========================================
There are some helper scripts used in the programe.

Run the following command to list the different scripts:

::

    python3 helper.py -h


Run the scripts with the ``-i`` switcher, we have used ``init`` to do something for initialization.

- ``migrate`` : for database schema change.
- ``edit_diff`` : send email for modification of the posts and pages.
- ``sitemap`` : would generate the sitemap for posts and pages.
- ``check_kind`` : to check if the kind of post is right.
- ``check`` : generate the picture for the relationship of templates. For example:

::

    python3 helper.py -i check templates/theme

would generate the picture for the relationship of the template files.

Unit Tests
=========================================

First you should install ``pytest``, ``coverage`` and ``pytest-cov`` with ``pip`` ,

::

   pip3 install pytest pytest-cov coverage

then run as follow:

::

   python3 -m pytest torcms/tests --cov=./torcms/tests --cov-report=html


Build the API documents
========================================

under TorCMS

::

    sphinx-apidoc -F -o api_doc torcms

Editing  ``api_doc/conf.py``. Add the following line after ``import sys``.

::

    sys.path.insert(0, os.path.abspath('../'))

That's OK. then generate the HTML documents. Under TorCMS:

::

    sphinx-build -b html api_doc api_html

Publish to PyPi
===============================================

First, build the distribution.

::

    python setup.py sdist

Then, upload to the website.

::

    twine upload dist/torcms-version.tar.gz