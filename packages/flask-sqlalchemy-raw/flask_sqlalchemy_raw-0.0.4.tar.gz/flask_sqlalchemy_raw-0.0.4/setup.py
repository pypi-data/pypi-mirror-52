# !/usr/bin/env python
# coding: utf-8

from setuptools import find_packages
from setuptools import setup

install_requires = [
    'pampy',
    'blinker'
]

setup(
    name='flask_sqlalchemy_raw',
    version='0.0.4',
    description="flask_sqlalchemy execute raw sql",
    packages=find_packages(),
    install_requires=install_requires,
    include_package_data=True,
)

