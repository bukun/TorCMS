#!/usr/bin/env python2
# -*- coding:utf-8 -*-
from setuptools import setup, find_packages

setup(
    name='torcms',
    version='0.5.5',
    keywords=('torcms', 'tornado', 'cms',),
    description='''CMS based on Python 3 and Tornado. Flexible, extensible web CMS framework built on Tornado and Peewee, compatible with Python 3.4 and 3.5.''',
    long_description=''.join(open('README.rst').readlines()),
    license='MIT License',

    url='https://github.com/bukun/TorCMS',
    # download_url = 'https://github.com/peterldowns/mypackage/tarball/0.1', #
    author='bukun',
    author_email='bukun@osgeo.cn',


    # packages=find_packages(exclude=["maplet.*", "maplet"]),
    packages=find_packages(exclude=["tester", "torcms_tester"]),

    platforms='any',
    zip_safe=True,
    install_requires=['beautifulsoup4', 'jieba', 'markdown', 'peewee', 'Pillow',
        'tornado', 'Whoosh', 'WTForms', 'wtforms-tornado','psycopg2','html2text', 'redis', 'pyyaml'],

    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 3 - Alpha',

        # Indicate who your project is intended for
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',

        # Pick your license as you wish (should match "license" above)
        'License :: OSI Approved :: MIT License',

        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5'
    ],
)
