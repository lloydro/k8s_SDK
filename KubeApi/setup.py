#!/usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = 'wangyc'
# __time__ = 2018/2/7 23:18
# Copyright (c) 2018 ruijie Corp.
# All Rights Reserved.


from setuptools import setup
from setuptools import find_packages


setup(
    name="KubeApi",
    version="1.1.3", # 添加了get_pods_ip功能，提供创建容器与等待容器IP的功能分离选项
    author="wangyc",
    author_email="wangyongcheng@ruijie.com.cn",
    description="for auto test",
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4'
    ],
    zip_safe=False,
    entry_points={}
)
