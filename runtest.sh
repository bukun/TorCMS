#!/bin/sh

python3 -m pytest tester --cov=./tester --cov-report=html

# if which coverage > /dev/null; then
#     coverage run tester
#     coverage report
# else
#     python3 -m pytest tester
# fi
