#!/usr/bin/env python
# coding: utf-8

from __future__ import print_function

import setuptools

setuptools.setup(
    name='kanban',
    version='0.1',
    author='Luc Sinet',
    author_email='luc.sinet@gmail.com',
    description='Kanban application',
    long_description='A Kanban application in command line interface',
    long_description_content_type='text/markdown',
    url='https://github.com/Tastyep/Kanban',
    packages=setuptools.find_packages(),
    license='MIT',
    classifiers=[
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
 )
