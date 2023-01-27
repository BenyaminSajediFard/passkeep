#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan 27 00:21:32 2023

@author: blackvulture
"""

from setuptools import setup, find_packages

setup(name="database", packages=find_packages())
setup(name="secret", packages=find_packages("database"))
