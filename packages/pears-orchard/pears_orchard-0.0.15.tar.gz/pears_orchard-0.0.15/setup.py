#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep 16 22:08:39 2019

@author: abhijithneilabraham
"""

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pears_orchard",
    version="0.0.15",
    author="Aurelie Herbelot",
    author_email="aurelie.herbelot@cantab.net",
    description="A decentralized search engine which can be run in local machine without letting anyone know the details about your search",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/abhijithneilabraham/PeARS-orchard",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU Affero General Public License v3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.5',
)