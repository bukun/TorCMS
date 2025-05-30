#!/usr/bin/env bash

cp ../cfg_demo.py ./
cp ../doc/requirements.txt ./

podman build -t torcms-debian_testing -f Dockerfile_deb_testing

rm -f ../admin_torcms/migrations/00*.py

podman run -it -v  ..:/coding/TorCMS torcms-debian_testing bash -c \
  "/etc/init.d/postgresql start && sudo -u postgres psql -c \"CREATE ROLE torcms WITH LOGIN PASSWORD '111111';\" && sudo -u postgres psql -c \"CREATE DATABASE torcms WITH OWNER torcms;\" && /vpy/bin/python manage.py makemigrations && /vpy/bin/python manage.py migrate && /vpy/bin/python3 helper.py -i init && /vpy/bin/python3 -m pytest torcms/tests"

rm -f *.py *.txt
