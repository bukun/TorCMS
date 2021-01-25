# Makefile, useful for developers only.
# Make sure you have pycodestyle and tox python modules installed.

.PHONY: clean lint test dist

all: lint test clean

clean:
	@find . -name '*.pyc' |xargs rm -f
	@find . -name '*.pyo' |xargs rm -f
	@find . -name '*.orig' |xargs rm -f
	@rm -rf MANIFEST build dist .coverage .tox __pycache__ api_doc docs/_build *.egg-info

lint:
	@type pycodestyle >/dev/null 2>&1 || { echo >&2 "Please install pycodestyle package."; exit 1; }
	@pycodestyle -r --max-line-length=120 torcms && { echo >&2 "PEP8: congrats, everything is clean !"; }
	@python3 -m pylint torcms && { echo >&2 "PEP8: congrats, everything is clean !"; }

test:
	@type tox >/dev/null 2>&1 && { tox; } || { python3 -m pytest tester --cov=./tester --cov-report=html; }

dist: clean
	@python setup.py register
	@python setup.py sdist upload
	@python setup.py bdist_wheel upload

api_doc: clean
	@sphinx-apidoc -F -o api_doc torcms
	@cd api_doc && { make html; }

env:
	@python3 -m venv env
	@./env/bin/python3 -m pip install -r doc/requirements.txt
	@./env/bin/python3 -m pip install -r doc/requirements_dev.txt
