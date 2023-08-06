#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import find_packages, setup

setup(
    name='kslabs-scrapy-heroku',
    version=":versiontools:kslabs_scrapy_heroku:",
    description="Utilities for running scrapy on heroku",
    long_description="",
    keywords='scrapy, heroku',
    author='Dave McLain',
    author_email='dave@trainca.se',
    url='https://github.com/Keystone-Strategy/kslabs-scrapy-heroku',
    license='BSD',
    include_package_data=True,
    packages=find_packages(),
    install_requires=[
        'scrapy',
        'psycopg2',
    ],
    setup_requires=[
        'versiontools >= 1.8',
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP',
    ])