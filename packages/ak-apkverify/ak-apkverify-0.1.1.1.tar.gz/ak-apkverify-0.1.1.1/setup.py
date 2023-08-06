#!/usr/bin/python
# coding=utf-8

from __future__ import absolute_import, unicode_literals

from setuptools import setup
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

__title__ = 'ak-apkverify'
__description__ = 'Appknox Fork - Jar Signature / APK Signature v2 verify with pure python (support rsa dsa ecdsa).'
__url__ = 'https://github.com/shuxin/apk-signature-verify'
__version__ = '0.1.1.1'
__author__ = 'shuxin'
__author_email__ = 'shuxin@users.noreply.github.com'
__license__ = 'MIT License'

with open(path.join(here, 'README.md'), 'r', encoding='utf-8') as f:
    readme = f.read()

setup(
    name=__title__,
    version=__version__,
    description=__description__,
    long_description=readme,
    long_description_content_type='text/markdown',
    author=__author__,
    author_email=__author_email__,
    url=__url__,
    license=__license__,
    packages=['apkverify'],
    python_requires='>=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*',
    install_requires=['asn1crypto>=0.24.0'],
    include_package_data=False,
    platforms='any',
    keywords=['apk', 'signature', 'verify'],
    zip_safe=False,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: POSIX',
        'Operating System :: POSIX :: BSD',
        'Operating System :: POSIX :: Linux',
        'Operating System :: Microsoft :: Windows',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy'
    ],
)
