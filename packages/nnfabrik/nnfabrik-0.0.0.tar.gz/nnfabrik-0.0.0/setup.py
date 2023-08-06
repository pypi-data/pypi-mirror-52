#!/usr/bin/env python
from setuptools import setup, find_packages
from os import path
import sys

here = path.abspath(path.dirname(__file__))

long_description = "Factory for fitting diverse collection of NNs on datasets" 

setup(
    name='nnfabrik',
    version="0.0.0",
    description="Neural Network factory pipelines",
    author='Konstantin Willeke, Edgar Y. Walker',
    license="MIT",
    packages=find_packages(exclude=[]),
    install_requires=[],
)
