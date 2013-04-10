#!/usr/bin/env python
# coding: utf-8

import os
import sys
import re

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(
    name='sandook',
    version='0.1',
    packages=['sandook', 'sandook.view', 'sandook.model', 'sandook.app', 'sandook.config'],
    url='http://ubhisat.github.io/Sandook/',
    license='MIT',
    author='Satmeet Ubhi',
    author_email='',
    description='Command line todo list',
    scripts=['scripts/sandook', 'scripts/sandook-config'],
    install_requires=['urwid', 'dropbox', 'argparse'],
)

