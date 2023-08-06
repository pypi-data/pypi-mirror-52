#!/usr/bin/env python
import os
from setuptools import setup
from setuptools import find_packages

# ----------------------------------------------------------------------------
# Building
#
# Create source distribution:
# ./setup.py sdist
#
#
# Create binary distribution (non-univeral, python 3 only):
# ./setup.py bdist_wheel --python-tag=py3
#
# Register on PyPI:
# twine register dist/mypkg.whl
#
#
# Upload to PyPI:
# twine upload dist/*
#
# ----------------------------------------------------------------------------

# project version
from shiftuser.version import version as package_version

# development status
# dev_status = '1 - Planning'
# dev_status = '2 - Pre-Alpha'
# dev_status = '3 - Alpha'
dev_status = '4 - Beta'
# dev_status = '5 - Production/Stable'
# dev_status = '6 - Mature'
# dev_status = '7 - Inactive'

# github repository url
repo = 'https://github.com/projectshift/shift-user'
license_type = 'MIT License'

description = 'User management, registration authentication and authorisation component for shiftboiler.'

# readme description
long_description = description
if os.path.isfile('README-PyPi.md'):
    with open('README-PyPi.md') as f:
        long_description = f.read()

# run setup
setup(**dict(

    # author
    author='Dmitry Belyakov',
    author_email='dmitrybelyakov@gmail.com',

    # project meta
    name='shiftuser',
    version=package_version,
    url=repo,
    download_url=repo + '/archive/' + package_version + '.tar.gz',
    description=description,
    long_description=long_description,
    long_description_content_type='text/markdown',  # This is important!
    keywords=[
        'python3',
        'flask',
        'click',
        'users',
        'auth',
        'rbac',
        'oauth2',
    ],

    # classifiers
    # see: https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[

        # maturity
        'Development Status :: ' + dev_status,

        # license
        'License :: OSI Approved :: ' + license_type,

        # audience
        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',

        # pythons
        'Programming Language :: Python :: 3',

        # categories
        'Environment :: Console',
        'Environment :: Web Environment',
        'Framework :: Flask',
        'Framework :: IPython',
        'Topic :: Internet :: WWW/HTTP :: Site Management',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
        'Topic :: Utilities'
    ],

    # project packages
    packages=find_packages(exclude=['tests*', 'migrations*']),

    # include none-code data files from manifest.in (http://goo.gl/Uf0Yxc)
    include_package_data=True,

    # # project dependencies
    install_requires=[
        'shiftboiler>=0.8.0,<0.9.0',
        'click>=7.0.0,<8.0.0',
        'bcrypt>=3.1.6,<4.0.0',
        'passlib==1.7.1',
        'PyJWT>=1.7.1,<2.0.0',
        'Flask-Login==0.4.1',
        'requests-oauthlib==1.1.0',
        'Flask-OAuthlib==0.9.5',
        'Flask-Principal==0.4.0'
    ],


    # project license
    license=license_type
))
