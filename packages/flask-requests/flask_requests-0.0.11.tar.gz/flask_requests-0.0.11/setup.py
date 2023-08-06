# !/usr/bin/env python
# coding: utf-8

from setuptools import find_packages
from setuptools import setup

install_requires = [
    'pampy',
    'blinker'
]

setup(
    name='flask_requests',
    version='0.0.11',
    description="egret, flask authentication used mongodb stored",
    packages=find_packages(),
    install_requires=install_requires,
    include_package_data=True,
)

