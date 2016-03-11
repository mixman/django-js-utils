from os import system
from os.path import dirname, join
from setuptools import setup
from distutils.core import Command

import django_js_utils

import os, sys, subprocess

class TestCommand(Command):
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        raise SystemExit(
            subprocess.call([sys.executable,
                             'app_test_runner.py',
                             'test']))

install_requires = [
    'six',
]

tests_require = [
    'Django',
    'nose',
    'coverage',
]

setup_requires = []

with open('README.md') as readmefile:
    long_description = readmefile.read()

setup(
    name='django-js-utils-nextgen',
    version=django_js_utils.__versionstr__,
    description='Django JS Urls: urlpatterns for clientside',
    long_description=long_description,
    author='Marco Louro, Jussi Vaihia',
    author_email='jussi.vaihia@gmail.com',
    url='https://github.com/mixman/django-js-utils',

    packages=['django_js_utils',],
    license='MIT',
    include_package_data=True,

    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Framework :: Django",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],

    cmdclass = {
        'test': TestCommand,
    },

    install_requires=install_requires,
    test_suite='nose.collector',
    tests_require=tests_require,
    setup_requires=setup_requires
)
