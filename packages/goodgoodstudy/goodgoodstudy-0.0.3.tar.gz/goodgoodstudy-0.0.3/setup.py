#!/usr/bin/env python
# coding: utf-8

from setuptools import setup

setup(
    name='goodgoodstudy',
    version='0.0.3',
    author='gyk001',
    author_email='gyk001@gmail.com',
    url='https://github.com/gyk001',
    description=u'好好学习',
    packages=['goodgoodstudy'],
    install_requires=[],
    entry_points={
        'console_scripts': [
            'goodgoodstudy=goodgoodstudy:goodgoodstudy',
            'goodgoodstudythen=goodgoodstudy:daydayup'
        ]
    }
)