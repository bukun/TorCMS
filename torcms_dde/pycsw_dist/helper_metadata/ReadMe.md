# 元数据相关

## 系统中的设计

pycsw元数据表为 records.

在TorCMS中，重新导入数据作为应用。 identifier 暂保存为 tabpost 表中的 memo 字段。

## 元数据请求测试

https://ddemd.deep-time.org/dcsw/pycsw?mode=opensearch&service=CSW&version=2.0.2&request=GetCapabilities


## 元数据收割测试的网址：

https://www.osgeo.cn/geonetwork/annexes/gallery/gallery.html

### 收割WMS存在的问题

如果在ＷＭS中未设置 `contact` ，在 pycsw 中会出错。

```
  File "/home/bk/vpy_csw/lib/python3.9/site-packages/pycsw-3.0.dev0-py3.9.egg/pycsw/core/metadata.py", line 351, in _parse_wms
    _set(context, serviceobj, 'pycsw:Creator', md.provider.contact.name)
AttributeError: 'NoneType' object has no attribute 'name'
```

不好的解决方法：将赋值的地方先注释掉。

## pycsw 说明

```
http://39.100.254.142:6627/pycsw/pycsw.py?service=CSW&version=3.0.0&request=GetCapabilities
http://39.100.254.142:6627/pycsw/pycsw.py?service=CSW&version=3.0.0&request=GetRecords&CONSTRAINTLANGUAGE=FILTER&typeNames=csw30:Record&outputFormat=application/json
http://39.100.254.142:6627/pycsw/pycsw.py?service=CSW&version=3.0.0&request=GetRecordById&id=urn:uuid:1ef30a8b-876d-4828-9246-c37ab4510bbd
http://39.100.254.142:6627/pycsw/pycsw.py?service=CSW&version=3.0.0&request=GetRecordById&id=urn:uuid:1ef30a8b-876d-4828-9246-c37ab4510bbd&elementSetName=full
http://39.100.254.142:6627/pycsw/pycsw.py?id=urn:uuid:94bc9c83-97f6-4b40-9eb8-a8e8787a5c63&elementSetName=full&request=GetRecordById&service=CSW&version=3.0.0
http://39.100.254.142:6627/pycsw/pycsw.py?service=CSW&version=2.0.2&request=GetCapabilities&mode=sru
http://39.100.254.142:6627/pycsw/pycsw.py?mode=sru&operation=searchRetrieve&query=a
http://39.100.254.142:6627/pycsw/pycsw.py?service=CSW&version=2.0.2&request=GetCapabilities&mode=opensearch
http://39.100.254.142:6627/pycsw/pycsw.py?mode=oaipmh&verb=Identify
```



http://39.100.254.142:6627/pycsw/pycsw.py?service=CSW&version=2.0.2&request=GetCapabilities

39.100.254.142:6627/pycsw/pycsw.py?service=CSW&version=2.0.2&request=GetRecords&CONSTRAINTLANGUAGE=FILTER&typeNames=csw:Record&ElementSetName=full

http://39.100.254.142:6627/pycsw/pycsw.py?service=CSW&version=2.0.2&request=GetRecords&CONSTRAINTLANGUAGE=FILTER&typeNames=csw:Record&ElementSetName=full&DistributedSearch=1&hopCount=2


https://ddemd.deep-time.org/dcsw.py?service=CSW&version=3.0.0&request=GetRecords&CONSTRAINTLANGUAGE=FILTER&typeNames=csw:Record&ElementSetName=full

constraintlanguage=urn:ogc:def:queryLanguage:OGC-CSW:CQLTEXT&constraint="csw:AnyText Like '%数%'"

http://39.100.254.142:6627/pycsw/pycsw.py?service=CSW&version=2.0.2&request=GetRecordById&id=urn:uuid:19887a8a-f6b0-4a63-ae56-7fba0e178010




http://39.100.254.142:6627/pycsw/pycsw.py?service=CSW&version=3.0.0&request=GetCapabilities


http://39.100.254.142:6627/pycsw/pycsw.py?service=CSW&version=3.0.0&request=GetRecords&CONSTRAINTLANGUAGE=FILTER&typeNames=csw30:Record&DistributedSearch=1&hopCount=2

http://39.100.254.142:6627/pycsw/pycsw.py?service=CSW&version=3.0.0&request=GetRecords&CONSTRAINTLANGUAGE=FILTER&typeNames=csw30:Record&DistributedSearch=1&hopCount=2


39.100.254.142:6627/pycsw/pycsw.py?service=CSW&version=3.0.0&request=GetRecords&CONSTRAINTLANGUAGE=FILTER&typeNames=csw30:Record&ElementSetName=full&DistributedSearch=1&hopCount=2&maxRecords=5&startPosition=5

https://ddemd.deep-time.org/dcsw.py?&service=CSW&version=3.0.0&request=GetRecords&CONSTRAINTLANGUAGE=FILTER&typeNames=csw30:Record&DistributedSearch=1&hopCount=2&ElementSetName=full&maxRecords=5&startPosition=1

https://ddemd.deep-time.org/dcsw.py?&service=CSW&version=3.0.0&request=GetRecords&CONSTRAINTLANGUAGE=FILTER&typeNames=csw30:Record&ElementSetName=full&maxRecords=5&startPosition=1

39.100.72.56:6627/pycsw/pycsw.py?service=CSW&version=3.0.0&request=GetRecordById&id=urn:uuid:19887a8a-f6b0-4a63-ae56-7fba0e178010

39.100.254.142:6627/pycsw/pycsw.py?service=CSW&version=3.0.0&request=GetRecordById&id=urn:uuid:19887a8a-f6b0-4a63-ae56-7fba0e178010&distributedsearch=TRUE


The csw:ElementySetName element specifies a mode (brief, summary, or full); the csw:ElementName element does not specify a mode, but just the name of a queryable element.


---


pycsw 4分钟安装教程


# Setup a virtual environment:
```
python3 -m venv ~/vpy_csw && . ~/vpy_csw/bin/activate && pip3  install wheel
```
mkdir ~/deploy/ &&  cd ~/deploy
# git clone https://github.com/geopython/pycsw.git && cd pycsw
```
git clone https://gitee.com/gislite/pycsw.git && cd pycsw
pip install -e . && pip install -r requirements-standalone.txt
```

# Create and adjust a configuration file:
```
cp default-sample.cfg default.cfg
```
vi default.cfg
# adjust paths in
# - server.home   #  /home/bk/deploy/pycsw
# - repository.database #修改路径   
# database=sqlite:////home/wdcrre/deploy/pycsw/metadb/cite.db
# - repository.database #修改路径   
database=sqlite:////home/bk/deploy/pycsw/metadb/cite.db
# set server.url to http://localhost:8000/   #  url=  http://localhost:8000/pycsw/csw.py
# Setup the database:
mkdir -p ~/deploy/pycsw/metadb
# pycsw-admin.py -c setup_db -f default.cfg
# 最新版本
```
pycsw-admin.py setup-db -c default.cfg
```
# Load records by indicating a directory of XML files, use -r for  recursive:
# pycsw-admin.py -c load_records -f default.cfg -p /path/to/xml/
# pycsw-admin.py -c load_records -f default.cfg -p  tests/functionaltests/suites/apiso/data
# 最新版本，如下：
```
pycsw-admin.py load-records -c default.cfg -p  ./tests/functionaltests/suites/cite/data/
```

# Export
mkdir /tmp/xx_meta
pycsw-admin.py -c export_records -f default.cfg -p /tmp/xx_meta
# Run the server:
$ python3 ./pycsw/wsgi.py
# See that it works!

