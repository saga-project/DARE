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
    package_dir={'': 'dare'},
    data_files=['dare.conf'],
    package_data={'': ['*.cfg'], '': ['*.cu'], 'dare': ['daredb/*.cu'],
                 'dare': ['daredb/*.cfg']},
    install_requires=['bigjob'],
    entry_points={'console_scripts': ['dare-run = dare.bin.darerun:main']})
