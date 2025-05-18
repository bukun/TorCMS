#!/usr/bin/env bash

python3 -m pytest torcms/tests --cov=./torcms/tests --cov-report=html
