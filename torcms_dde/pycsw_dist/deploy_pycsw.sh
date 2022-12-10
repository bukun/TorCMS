# 安装于Ubuntu 22.04.

sudo apt install -y libxml2-dev libxslt1-dev liblzma-dev python3-lxml \
  libgeos-dev zlib1g-dev libevent-dev

# 如果要使用 PostgreSQL数据库
sudo apt install -y postgis postgresql-plpython3-14

# Setup a virtual environment:

if [ -d "~/usr/vpy_csw" ]; then
  echo 'venv exists.'
else
  python3 -m venv --clear ~/usr/vpy_csw \
    && . ~/usr/vpy_csw/bin/activate \
    && pip3 install wheel \
    && pip3 install psycopg2-binary
fi

# git clone https://github.com/geopython/pycsw.git && cd pycsw

the_pwd=`pwd`


if [ -d "$the_pwd/zz_pycsw_drr" ]; then
    cd $the_pwd/zz_pycsw_drr && git reset --hard && git clean -fd && git pull
else
    cd $the_pwd && git clone https://gitee.com/gislite/pycsw.git $the_pwd/zz_pycsw_drr
fi

if [ -d "$the_pwd/zz_pycsw_wdc" ]; then
    cd $the_pwd/zz_pycsw_wdc && git reset --hard && git clean -fd && git pull
else
    cd $the_pwd && git clone https://gitee.com/gislite/pycsw.git $the_pwd/zz_pycsw_wdc
fi


cd $the_pwd/zz_pycsw_wdc && pip install -e . && pip install -r requirements-standalone.txt




