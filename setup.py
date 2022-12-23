# -*- coding:utf-8 -*-

'''
For pypi
'''

from setuptools import find_packages, setup

desc = ('Flexible, extensible Web CMS framework built on Tornado,'
        'compatible with Python 3.7 and above.')
setup(
    name='torcms',
    version='0.8.9',
    keywords=['torcms', 'tornado', 'cms'],
    description=desc,
    long_description=''.join(open('README.rst').readlines()),
    license='MIT License',

    url='https://github.com/bukun/TorCMS',
    author='bukun',
    author_email='bukun@osgeo.cn',

    packages=find_packages(
        # include=('torcms',),
        exclude=('devops', "tester", "torcms_tester", 'flasky', 'torcms_*')),
    include_package_data=True,

    platforms='any',
    zip_safe=True,
    install_requires=['beautifulsoup4', 'jieba', 'markdown',
                      'peewee', 'Pillow', 'wheel',
                      'tornado', 'Whoosh', 'WTForms',
                      'tornado-wtforms', 'email-validator',
                      'psycopg2-binary', 'html2text',
                      'redis', 'pyyaml', 'htmlmin'],

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
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
    ],
)
