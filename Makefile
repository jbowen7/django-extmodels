###################################################################
# Makefile for django project
#
# useful targets:
#   make build           ----------------- builds an env to work in
#   make destroy         ----------------- destroys the virtualenv
#   make package         ----------------- builds dist package
#   make distribute      ----------------- distributes via twine to pypi
#   make clean           ----------------- cleans everything created from runtime and testing
#   make tests           ----------------- runs all tests, linters and coverage
#   make lint            ----------------- run linter against source code
#   make format          ----------------- run code formatters (iSort)
#
#
#
#
###################################################################


PYTHON := env/bin/python
MANAGE := env/bin/manage.py
PIP := env/bin/pip
TOX := env/bin/tox
ISORT := env/bin/isort

.PHONY: build
build: build-env

.PHONY: build-env
build-env:
	/usr/bin/env python3.6 -m venv env
	$(PYTHON) -m pip install --upgrade pip
	#$(PYTHON) -m pip install -e .

.PHONY: destroy
destroy: clean
	rm -fr env

.PHONY: package
package:
	$(PYTHON) setup.py sdist bdist_wheel

.PHONY: distribute
distribute:
	$(PYTHON) -m twine upload dist/*

.PHONY: clean
clean: clean-pyc clean-tests clean-egg

.PHONY: clean-pyc
clean-pyc:
	find . -name '*.pyc' | xargs /bin/rm -f

.PHONY: clean-egg
clean-egg:
	find . -type d -name '*egg-info' | xargs /bin/rm -fr

.PHONY: clean-tests
clean-tests:
	/bin/rm -fr .tox

.PHONY: freeze
freeze:
	$(PYTHON) -m pip freeze --exclude-editable > requirements.txt

.PHONY: tests
tests:
	$(TOX)

.PHONY: lint
lint:
	$(TOX) -e flake8

.PHONY: format
format:
	$(ISORT) -rc src/
