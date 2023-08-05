#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
from setuptools import find_packages, setup

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'nas'))
from version import __version__ as version

setup(
    name='nas',
    version=version,
    description='a library of network architecture search',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Zhiqing Xiao',
    author_email='xzq.xiaozhiqing@gmail.com',
    url='http://github.com/zhiqingxiao/nas/',
    packages=find_packages(),
    include_package_data=True,
    classifiers=[
        'Programming Language :: Python',
        'Intended Audience :: Science/Research',
    ],
)
