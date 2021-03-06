#!/usr/bin/env python3
# coding: utf-8

from setuptools import setup
from setuptools import find_packages

from jmm import VERSION

with open('jmm/requirements.txt', 'r', encoding='utf8') as file:
    install_requires = list(map(lambda x: x.strip(), file.readlines()))


setup(
    name='jmm',
    version=VERSION,
    author='kinopico',
    author_email='zqmillet@qq.com',
    url='https://github.com/zqmillet/japanese_media_manager',
    description='a cli tool for management of japanese adult media',
    packages=find_packages(),
    install_requires=install_requires,
    entry_points={
        'console_scripts': [
            'jmm=jmm.scripts.entry_point:main',
        ]
    }
)
