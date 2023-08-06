#!/usr/bin/env python
import os

from setuptools import setup

SCRIPT_DIR = os.path.dirname(__file__)
if not SCRIPT_DIR:
    SCRIPT_DIR = os.getcwd()


setup(
    name="conversion",
    use_scm_version=True,
    description="Utility functions to convert strings to Python types",
    author="Roberto Aguilar",
    author_email="r@rreboto.com",
    packages=["conversion"],
    long_description=open("README.md").read(),
    url="http://github.com/rca/conversion",
    license="LICENSE",
)
