#!/usr/bin/env python
# coding: utf-8

from setuptools import setup
setup(
    name='bloodstone-core',
    version='0.0.1',
    author='zhangweiwang',
    author_email='zhangweiwang@pwrd.com',
    url="https://x.wanmei.com",
    description=u'common util of pwrd python service',
    packages=['wmpy_util'],
    install_requires=[
        'Django',
        'tensorflow',
        'schedule',
        'numpy',
        'opencv-contrib-python'
    ],
    entry_points={
        'console_scripts': [
        ]
    }
)