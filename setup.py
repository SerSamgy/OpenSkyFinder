#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    Setup file for openskyfinder.

    This file was generated with PyScaffold 2.5.7, a tool that easily
    puts up a scaffold for your new Python project. Learn more under:
    http://pyscaffold.readthedocs.org/
"""

import sys

from setuptools import setup


def setup_package():
    needs_sphinx = {'build_sphinx', 'upload_docs'}.intersection(sys.argv)
    sphinx = ['sphinx'] if needs_sphinx else []
    setup(
        setup_requires=['pytest-runner'] + sphinx,
        tests_require=['pytest', 'pytest-cov'],
        install_requires=['haversine==0.4.5', 'requests==2.13.0'],
        # packages=find_packages()
    )


if __name__ == "__main__":
    setup_package()
