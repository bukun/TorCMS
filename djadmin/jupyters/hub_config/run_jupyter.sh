#! /bin/bash

python3 -m venv --clear ./vpy_jupyter
. ./vpy_jupyter/bin/activate
pip install -r requirements.txt

#export OAUTH2_AUTHORIZE_URL="http://121.42.45.218:6795/o/authorize"
#export OAUTH2_TOKEN_URL="http://121.42.45.218:6795/o/token/"
#export OAUTH2_USERDATA_URL="http://121.42.45.218:6795/userdata"
#export JUPYTERHUB_CRYPT_KEY=$(openssl rand -hex 32)

#vpyenv=/home/bk/usr/vpy_django/bin/python

jupyterhub -f jupyterhub_config.py

