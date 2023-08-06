# !/usr/bin/env python
# coding: utf-8

from setuptools import find_packages
from setuptools import setup

install_requires = [
    'nezha'
]

setup(
    name='flask_hooks',
    version='0.0.2',
    description="flask hook tools",
    packages=find_packages(),
    install_requires=install_requires,
    include_package_data=True,
)

