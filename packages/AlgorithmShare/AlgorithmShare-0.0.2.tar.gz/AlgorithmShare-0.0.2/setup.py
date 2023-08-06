#!/usr/bin/env python
# coding: utf-8

from setuptools import setup

setup(
    name='AlgorithmShare',
    version='0.0.2',
    author='qinwei',
    author_email='qinwei17@otcaix.iscas.ac.cn',
    url='http://earthdataminer.casearth.cn',
    description='Shared Algorithm Lib',
    packages=['AlgorithmShare'],
    install_requires=[
		'requests',
		'urllib3'
	]
)
