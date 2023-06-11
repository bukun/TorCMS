Introduction
======================================

原为独立项目。合并到 TorCMS 中。

Help to convert any metadata in "dict" into pycsw database.


For pycsw
=================================

Install libs Under Debian
--------------------------------------------------

::

    apt install -y libxml2-dev libxslt1-dev liblzma-dev python3-lxml libgeos-dev
    apt install -y libxml2-dev libxslt1-dev python-dev python3-dev
    apt install -y zlib1g-dev
    apt install -y libevent-dev

Install for Python
----------------------------------------

.. pycsw in 4 minutes.

::
    
    # Setup a virtual environment:
    python3 -m venv vpy_csw && cd vpy_csw && . bin/activate && pip3 install wheel
    mkdir ~/deploy/ &&  cd ~/deploy
    git clone https://github.com/geopython/pycsw.git && cd pycsw
    pip install -e . && pip install -r requirements-standalone.txt
    
    # Create and adjust a configuration file:
    cp default-sample.cfg default.cfg
    vi default.cfg


adjust paths in
--------------------------------------------

::

    # - server.home   #  /home/bk/deploy/pycsw
    # - repository.database #修改路径   database=sqlite:////home/wdcrre/deploy/pycsw/metadb/cite.db
    # - repository.database #修改路径   database=sqlite:////home/bk/deploy/pycsw/metadb/cite.db
    # set server.url to http://localhost:8000/   #  url=http://localhost:8000/pycsw/csw.py
    
Setup the database:
---------------------------------------------------

::

    mkdir -p /home/wdcrre/deploy/pycsw/metadb
    
    pycsw-admin.py -c setup_db -f default.cfg
    
    # Load records by indicating a directory of XML files, use -r for recursive:
    pycsw-admin.py -c load_records -f default.cfg -p /path/to/xml/
    
    pycsw-admin.py -c load_records -f default.cfg -p tests/functionaltests/suites/apiso/data
    
    # Export
    mkdir /tmp/xx_meta
    pycsw-admin.py -c export_records -f default.cfg -p /tmp/xx_meta


Run the server:
--------------------------------------------------------------------------

::

    $ python ./pycsw/wsgi.py

See that it works!
-------------------------------------------

::

    $ curl http://0.0.0.0:8000/?service=CSW&version=2.0.2&request=GetCapabilities

http://0.0.0.0:8000/?service=CSW&request=GetCapabilities

http://0.0.0.0:8000/?service=CSW&version=2.0.2&request=GetCapabilities

Access via HTTP
---------------------------------------------

cp tests/suites/cite/data/cite.db /tmp

CSW version 3.0.0

http://0.0.0.0:8000/csw?mode=sru&operation=searchRetrieve&query=&maximumRecords=5&startRecord=0

http://0.0.0.0:8000/csw?service=CSW&version=3.0.0&request=GetRecordById&ElementSetName=full&Id=urn:uuid:d28cde50-85d9-11e8-a5c4-00163e05d7bfi

In Json format

http://0.0.0.0:8000/csw?service=CSW&version=3.0.0&request=GetRecordById&ElementSetName=full&Id=wdcrre-95285&outputFormat=application/json
