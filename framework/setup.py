#!/usr/bin/env python

from setuptools import setup, find_packages
import distribute_setup
distribute_setup.use_setuptools()

import dare


setup(name='DARE',
    version=dare.__version__,
    description='Dynamic Application Runtime Environment',
    author='Sharath Maddineni',
    author_email='smaddineni@cct.lsu.edu',
    maintainer="Sharath Maddineni",
    maintainer_email="smaddineni@cct.lsu.edu",
    url='https://github.com/saga-project/DARE',
    license="MIT",
    packages=['dare', 'dare/bin', 'dare/core', 'dare/helpers', 'dare/daredb'],
    package_data={'dare': ['daredb/*']},
    install_requires=['bigjob'],
    entry_points={'console_scripts': ['dare-run = dare.bin.darerun:main']})
