#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from setuptools import setup, find_packages

import monkey.ioc

project_dir = os.path.dirname(os.path.realpath(__file__))
requirement_file_path = project_dir + '/requirements.txt'
requirements = []
if os.path.isfile(requirement_file_path):
    with open(requirement_file_path) as f:
        requirements = f.read().splitlines()

setup(
    name=monkey.ioc.__name__,
    version=monkey.ioc.__version__,
    author=monkey.ioc.__author__,
    author_email=monkey.ioc.__author_email__,
    url='https://bitbucket.org/monkeytechnologies/monkey-ioc/',
    description='Simple IOC framework agile as a monkey.',
    long_description=open('README.rst').read(),
    license="Apache License, Version 2.0",

    packages=find_packages(exclude=['tests', 'samples']),
    include_package_data=True,
    install_requires=requirements,

    classifiers=[
        'Programming Language :: Python',
        'Development Status :: 1 - Planning',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.6',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Intended Audience :: Developers'
    ]
)
