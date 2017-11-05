#!/usr/bin/env python
# -*- encoding: utf-8 -*-
from glob import glob

from setuptools import find_packages
from setuptools import setup


setup(
    name='mocker',
    version='0.2.0',
    license='MIT',
    description='A simple HTTP mock server inspired by Saray',
    author='Paolo Ferretti',
    author_email='paolo.ferretti@fastmail.com',
    url='https://github.com/theghostwhocodes/mocker',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    py_modules=[splitext(basename(path))[0] for path in glob('src/*.py')],
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        # complete classifier list: http://pypi.python.org/pypi?%3Aaction=list_classifiers
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Environment :: Console',
        'Operating System :: Unix',
        'Operating System :: POSIX',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: Implementation :: CPython',
        'Topic :: Utilities',
    ],
    keywords=[
        'mock', 'stub', 'http', 'test'
    ],
    install_requires=[],
    extras_require={},
    entry_points={},
)
