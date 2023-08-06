#!/usr/bin/env python -*- coding: utf-8 -*-
#
# Copyright (C) 2020 alvations
# URL:
# For license information, see LICENSE.md

from distutils.core import setup

setup(
    name='subtitles',
    version='0.0.1',
    packages=['subtitles'],
    description='Python WSD',
    long_description='',
    url = 'https://github.com/alvations/subtitles',
    package_data={'pywsd': ['data/',]},
    license="MIT",
    install_requires = []
)
