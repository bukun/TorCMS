#!/usr/bin/env bash

podman build -t torcms-ubun24 -f Dockerfile_ubu24

rm -f ../admin_torcms/migrations/00*.py

podman run -it -v  ../../TorCMS:/coding/TorCMS bk-torcms-ubun24 bash -c \
  "/etc/init.d/postgresql start && sudo -u postgres psql -c \"CREATE ROLE torcms WITH LOGIN PASSWORD '111111';\" && sudo -u postgres psql -c \"CREATE DATABASE torcms WITH OWNER torcms;\" && /vpy/bin/python manage.py makemigrations && /vpy/bin/python manage.py migrate && /vpy/bin/python3 helper.py -i init && /vpy/bin/python3 -m pytest torcms/tests"

