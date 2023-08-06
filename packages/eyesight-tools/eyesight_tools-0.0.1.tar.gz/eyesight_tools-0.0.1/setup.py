#!/usr/bin/env python
#-*- coding:utf-8 -*-

#############################################
# File Name: setup.py
# Author: gm
# Mail: 1025304567@qq.com
# Created Time: 2019-04-11 15:37:04
#############################################


from setuptools import setup, find_packages

setup(
    name = "eyesight_tools",
    version = "0.0.1",
    keywords = ("pip", "eyesight","eyesight_tools", "tool", "gm"),
    description = "eyesight 相关工具类封装",
    long_description = "eyesight 相关工具类封装",
    license = "MIT Licence",

    url = "",
    author = "gm",
    author_email = "1025304567@qq.com",

    packages = find_packages(),
    include_package_data = True,
    platforms = "any",
    install_requires = ['chardet']
)