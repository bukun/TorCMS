# 安装于Ubuntu 22.04.

sudo apt install -y libxml2-dev libxslt1-dev liblzma-dev python3-lxml \
  libgeos-dev zlib1g-dev libevent-dev

# 如果要使用 PostgreSQL数据库
sudo apt install -y postgis postgresql-plpython3-14

# Setup a virtual environment:
python3 -m venv ./vpy_csw && . vpy_csw/bin/activate && pip3 install wheel && pip3 install psycopg2-binary

# git clone https://github.com/geopython/pycsw.git && cd pycsw
git clone https://gitee.com/gislite/pycsw.git

cd pycsw && pip install -e . && pip install -r requirements-standalone.txt




