# 参考： https://github.com/amutu/zhparser
# Ubuntu 22.04

sudo apt install postgresql-server-dev-14

# 安装 scws
wget -q -O - http://www.xunsearch.com/scws/down/scws-1.2.3.tar.bz2 | tar xjf -
cd scws-1.2.3 ; ./configure ; sudo make install

# 安装 zhparser
git clone https://github.com/amutu/zhparser.git
cd zhparser
make
sudo make install

