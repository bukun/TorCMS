#!/usr/bin/env bash

copy ../doc/requirements.txt ./xx_requirements.txt
copy ../doc/requirements-dev.txt ./xx_requirements-dev.txt

podman build -t torcms-debian11 Dockerfile_deb11

rm -f ./admin_torcms/migrations/00*.py

podman run -it -v  .:/coding/TorCMS torcms-debian11 bash -c \
  "/etc/init.d/postgresql start && sudo -u postgres psql -c \"CREATE ROLE torcms WITH LOGIN PASSWORD '111111';\" && sudo -u postgres psql -c \"CREATE DATABASE torcms WITH OWNER torcms;\" && /vpy/bin/python manage.py makemigrations && /vpy/bin/python manage.py migrate && /vpy/bin/python3 helper.py -i init && /vpy/bin/python3 -m pytest torcms/tests"


