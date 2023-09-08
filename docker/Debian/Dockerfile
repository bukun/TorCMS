FROM debian:11
# bullseye

MAINTAINER bukun <bukun@osgeo.cn>

# RUN echo     "en_US.UTF-8 UTF-8" > /etc/locale.gen
# RUN echo     "zh_CN.UTF-8 UTF-8" >> /etc/locale.gen
# RUN locale-gen
# ENV LANG en_US.UTF-8
# ENV LANGUAGE en_US:en
# ENV LC_ALL en_US.UTF-8

RUN echo "deb http://mirrors.163.com/debian/ bullseye main non-free contrib" > /etc/apt/sources.list
RUN echo "deb http://mirrors.163.com/debian/ bullseye-updates main non-free contrib" >> /etc/apt/sources.list
RUN echo "deb http://mirrors.163.com/debian-security bullseye-security main" >> /etc/apt/sources.list
RUN echo "deb http://mirrors.163.com/debian/ bullseye-backports main non-free contrib" >> /etc/apt/sources.list


#########################################
RUN mkdir ~/.pip
RUN echo "[global]" > ~/.pip/pip.conf
RUN echo "index-url = https://pypi.douban.com/simple" >> ~/.pip/pip.conf
RUN echo "[install]" >> ~/.pip/pip.conf
RUN echo "trusted-host=pypi.douban.com" >> ~/.pip/pip.conf
##############################################################################
RUN apt update
RUN apt -y dist-upgrade
RUN apt install -y git locales python3-pip redis-server python3-venv postgresql-server-dev-all libpq-dev

######################################

##############################################################################

# RUN cd /scipy && pip3 install scipy
# RUN cd /scipy/doc && make html

RUN ln -sf /bin/bash /bin/sh
# RUN useradd -ms /bin/bash  bk
########################################################

# USER bk

RUN python3 -m venv /vpy


RUN mkdir /coding
WORKDIR /coding

RUN git clone https://gitee.com/bukun/TorCMS.git

WORKDIR /coding/TorCMS

RUN git clone https://gitee.com/bukun/torcms_f2elib.git static/f2elib

RUN source /vpy/bin/activate && pip3 install wheel
RUN source /vpy/bin/activate && pip3 install email_validator
RUN source /vpy/bin/activate && pip3 install -r doc/requirements.txt
RUN source /vpy/bin/activate && pip3 install -r doc/requirements-dev.txt

# Add VOLUMEs to allow backup of config, logs and databases

# USER postgres
# Expose the PostgreSQL port

COPY cfg.py /coding/TorCMS
# RUN /vpy/bin/python3 helper.py -i init
