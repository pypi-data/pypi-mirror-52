#!/usr/bin/env python
# coding=utf-8

from setuptools import setup, find_packages

setup(
    name='NorrisUtils',
    version='1.1.3',
    description=(
        'norris'
    ),
    long_description=open('README.md').read(),
    author='AlaricNorris',
    author_email='norris.sly@gmail.com',
    maintainer='AlaricNorris',
    maintainer_email='norris.sly@gmail.com',
    license='BSD License',
    packages=find_packages(),
    platforms=["all"],
    url='https://www.baidu.com',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Operating System :: OS Independent',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python',
        'Programming Language :: Python :: Implementation',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Software Development :: Libraries'
    ],
    install_requires=[
        'requests>=2.19.1',
    ],
)