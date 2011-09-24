#!/usr/bin/env python


import sys, os
from setuptools import setup, find_packages


setup(
    name = 'portfolio', 
    version = '0.1',
    description='Django URL Exposure to Javascript',
    author='Dimitri Gnidash',
    author_email='dimitri.gnidash@gmail.com',
    url='https://github.com/Dimitri-Gnidash/django-js-utils',
    packages = find_packages(
        exclude = ['ez_setup', 'examples', 'tests']),
)
