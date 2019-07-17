#!/usr/bin/env python3

import os

from setuptools import find_packages, setup

NAME = 'django-extmodels'
VERSION = '0.1.1'


base_dir = os.path.dirname(__file__)
with open(os.path.join(base_dir, 'requirements.txt')) as f:
	install_requires = f.read().splitlines()

setup(
	name=NAME,
	version=VERSION,
	description='Extended the utility of Django Models',
	author='John Bowen',
	author_email='jbowen7@gmail.com',
	package_dir={'': 'src'},
	packages=find_packages(where='src', exclude=[]),
	install_requires=install_requires,
	python_requires='>=3.6',
	keywords=['django', 'dynamic', 'models'],
)
