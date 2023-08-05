#!/usr/bin/env python
# coding: utf-8

from setuptools import setup, find_packages

setup(
    name='bupt_api',
    version='0.0.4',
    author='zekin',
    author_email='wzekin@gmail.com',
    url='https://github.com/WangZeKun/bupt-api',
    description=u'北邮的一些api,陆续添加中',
    packages=find_packages(),
    include_package_data=True,
    platforms='any',
    install_requires=['beautifulsoup4', 'requests', 'ics'],
)
