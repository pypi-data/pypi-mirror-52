# !/usr/bin/env python
# coding: utf-8

from setuptools import find_packages
from setuptools import setup

install_requires = [
    'flask',
]

setup(
    name='flask_abort',
    version='0.0.1',
    description="flask abort",
    packages=find_packages(),
    install_requires=install_requires,
    include_package_data=True,
)
