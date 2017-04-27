#!/usr/bin/env python

from setuptools import setup

setup(
    name='curl-requests',
    version='0.1',
    description='replacement for `requests` using libcurl',
    author='Ben Longbons',
    author_email='b.r.longbons@gmail.com',
    url='https://github.com/o11c/python-curl-requests',
    packages=['curl_requests'],
    install_requires=['pycurl'],
)
