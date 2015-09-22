from os import system
from os.path import dirname, join
from setuptools import setup
from distutils.core import Command

import django_js_utils


install_requires = [
    'six',
]

tests_require = [
    'nose',
    'coverage',
]

setup_requires = []

with open('README.rst') as readmefile:
    long_description = readmefile.read()


class BumpVersion(Command):
    description = "Bump version automatically (by your CI tool)"
    user_options = [
        ('commit', None, 'Commit changed files to VCS (no push)'),
        ('tag', None, 'Create release tag in VCS (no push)'),
    ]
    boolean_options = ['commit', 'tag']

    def initialize_options(self):
        self.commit = False
        self.tag = False

    def finalize_options(self):
        pass

    def run(self):
        v = django_js_utils.__version__
        new_version = v[:-1] + (v[-1] + 1, )
        new_version_str = '.'.join(map(str, new_version))
        initfile = join(dirname(django_js_utils.__file__), '__init__.py')

        with open(initfile, 'r') as ifile:
            print("Reading old package init file...")
            istr = ifile.read()
            istr = istr.replace(str(v), str(new_version))

        with open(initfile, 'w') as ifile:
            print("Writing new init file with version %s..." % new_version_str)
            ifile.write(istr)

        if self.commit:
            print("Committing version file to VCS...")
            system('git commit %s -m "Version bump %s"' % (initfile, new_version_str))

        if self.tag:
            print("Creating tag r/%s in VCS..." % new_version_str)
            system('git tag r/%s' % new_version_str)



setup(
    name='django-js-utils-nextgen',
    version=django_js_utils.__versionstr__,
    description='Django URL Exposure to Javascript',
    long_description=long_description,
    author='Dimitri Gnidash, Jiri Suchan',
    author_email='dimitri.gnidash@gmail.com',
    url='https://github.com/mixman/django-js-utils',

    packages=('django_js_utils', ),
    license='BSD',
    include_package_data=True,

    cmdclass={
        'bump_version': BumpVersion,
    },

    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Framework :: Django",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],

    install_requires=install_requires,
    test_suite='nose.collector',
    tests_require=tests_require,
    setup_requires=setup_requires
)
