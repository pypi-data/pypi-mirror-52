# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

try:
    long_description = open("README.rst").read()
except IOError:
    long_description = ""

with open('requirements.txt') as fin:
    required = fin.read().splitlines()

setup(
    name="bambora",
    version="0.1.1",
    description="Bambora Client API",
    license="MIT",
    author="Loïc Faure-Lacroix",
    packages=find_packages(),
    include_package_data=True,
    install_requires=required,
    long_description=long_description,
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
    ]
)
