
安装步骤：

apt install postgresql postgis 


创建数据库后，在数据库中创建扩展

    create extension hstore;
    create extension postgis;
    CREATE EXTENSION plpython3u;

pycsw 使用

    export PYCSW_CONFIG=/home/bk/deploy/dde/pycsw/default.cfg


初始化数据库

    pycsw-admin.py setup-db -c default.cfg


加载元数据：

    pycsw-admin.py load-records -c default.cfg -p  ./tests/functionaltests/suites/cite/data/


pycsw-admin.py post-xml -u http://csw.deep-time.org/csw -x valid_fao.xml
pycsw-admin.py post-xml -u http://0.0.0.0:8000/csw -x valid_fao.xml



pycsw-admin.py load-records -c default.cfg -p  ~/deploy/dde/helper_metadata/xunhang/xx_xml/变质岩石学一级网巡卡片/
python pycsw/wsgi.py
pycsw-admin.py load-records -c default.cfg -p  /home/bk/deploy/dde/helper_metadata/xunhang/xx_xml/地层学


pip install pycsw
source ~/vpy_pycsw/bin/activate
~/vpy_pycsw/bin/act
~/vpy_pycsw/bin/ac
python pycsw/wsgi.py 6670
cd pycsw/
history  | grep pycsw-admin
python3 pycsw/wsgi.py 6670
git remote add upstream https://github.com/geopython/pycsw.git
git clone https://github.com/bukun/pycsw.git
python3 pycsw/wsgi.py  6670
python pycsw/wsgi.py  6670
vim pycsw/wsgi.py
vim pycsw/wsgi
vim ./pycsw/__init__.py
vim ./pycsw/wsgi.py
ls pycsw/
pip uninstall  pycsw
cp ../pycsw-3.0.0/default.cfg  ./
cd pycsw-2.6.1/
wget https://files.pythonhosted.org/packages/76/ba/cfa1a296910ce55c009a0e2e7e24480ed037d5c01f70456faaee3637d670/pycsw-2.6.1.tar.gz
pycsw
sudo apt install python3-pycsw
pycsw-admin.py load-records -c default.cfg -p  ./ds/
pycsw-admin.py setup-db --config default.cfg
cd pycsw-3.0.0/
vim ./pycsw/ogc/csw/csw2.py
pip install pycsw==2.6.1
cp ../pycsw-3.0.0/default.cfg ./
tar xfvz pycsw-2.6.1.tar.gz
mv pycsw pycsw-3.0.0

导入元数据的方式：

    pycsw-admin.py load-records -c default.cfg -p  ~/deploy/dde/xlsx2xml/xx_xml/


    
cd deploy/pycsw/
pycsw-admin.py setup-db --config default.cfgq
cd ../pycsw/
vim script_pycsw.py
python pycsw/wsgi
python3 pycsw/wsgi
git clone https://gitee.com/gislite/pycsw.git && cd pycsw
python3 flask_pycsw.py
pycsw-admin -c load_records -f default.cfg -p ../pycsw-src/tests/functionaltests/suites/cite/data/
pycsw-admin -c setup_db -f default.cfg
pycsw-admin.py -c setup_db -f default.cfg
ls ../pycsw/tests/functionaltests/suites/apiso/data/
ls ../pycsw/tests/functionaltests/suites/apiso/
ls ../pycsw/tests/functionaltests/suites/
ls ../pycsw/tests/functionaltests/suites/cite/data/
ls ../pycsw/
pycsw-admin -c load_records -f default.cfg -p ../pycsw/tests/functionaltests/suites/cite/data/
vim flask_pycsw.py
more flask_pycsw.py
pycsw-admin.py -c load_records -f default.cfg -p ../pycsw/tests/functionaltests/suites/cite/data/
pycsw-admin --help
pycsw-admin --hlep
cp ../pycsw/default-sample.cfg ./default.cfg
more ./pycsw/tests/functionaltests/suites/csw30/default.cfg
find ./pycsw/ | grep cfg
git clone https://gitee.com/gislite/pycsw.git
sudo apt install pycsw
apt search pycsw
