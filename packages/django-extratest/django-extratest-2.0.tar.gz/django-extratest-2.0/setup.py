#!/usr/bin/env python
#
# Copyright (C) 2015 Martin Owens
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
#
"""Setup for extratest module"""

import os

from setuptools import setup, find_packages

import extratest

# remove MANIFEST. distutils doesn't properly update it when the contents of directories change.
if os.path.exists('MANIFEST'):
    os.remove('MANIFEST')

with open('README.md') as fhl:
    README = fhl.read()

setup(
    name=extratest.__pkgname__,
    version=extratest.__version__,
    description=extratest.__doc__,
    long_description=README,
    url='https://gitlab.com/doctormo/django-extratest',
    author='Martin Owens',
    author_email='doctormo@gmail.com',
    platforms='linux',
    license='LGPLv3',
    packages=find_packages(),
    install_requires=[
        'django>=2.0',
    ],
)
