# -*- coding:utf-8 -*-
try:
    from setuptools import setup, find_packages
except:
    from distutils.core import setup
from codecs import open
from os import path

#版本号
VERSION = '0.0.2'

#发布作者
AUTHOR = "narcissu"

#邮箱
AUTHOR_EMAIL = "1791121094@qq.com"

#项目网址
URL = "https://github.com/narcisssujsk/iscsinar"

#项目名称
NAME = "iscsinar"

#项目简介
DESCRIPTION = "desc"

#LONG_DESCRIPTION为项目详细介绍，这里取README.md作为介绍
here = path.abspath(path.dirname(__file__))
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
     LONG_DESCRIPTION = f.read()

#搜索关键词
KEYWORDS = "iscsinar"

#发布LICENSE
LICENSE = "MIT"

#包
PACKAGES = ["iscsinar"]

#具体的设置
setup(
    name=NAME,
    version=VERSION,
    description=LONG_DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',

    ],
    #指定控制台命令
    entry_points={
        'console_scripts': [
  		'demo = iscsinar.demo:main',#pip安装完成后可使用demo命令调用demo下的main方法
        ],
    },
    keywords=KEYWORDS,
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    url=URL,
    license=LICENSE,
    packages=PACKAGES,
    install_requires=[],#依赖的第三方包
    include_package_data=True,
    zip_safe=True,
)
