#!/usr/bin/env python
# encoding: utf-8

from setuptools import setup, find_packages

setup(
    name='Recopytex',
    version='1.1',
    description='Assessment analysis',
    author='Benjamin Bertrand',
    author_email='',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'Click',
    ],
    entry_points='''
            [console_scripts]
            recopytex=recopytex.scripts.recopytex:cli
    ''',
    )

# -----------------------------
# Reglages pour 'vim'
# vim:set autoindent expandtab tabstop=4 shiftwidth=4:
# cursor: 16 del
