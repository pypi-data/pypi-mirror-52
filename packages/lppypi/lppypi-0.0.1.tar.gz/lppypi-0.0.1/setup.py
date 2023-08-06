# -*- coding:utf-8 -*-
try:
    from setuptools import setup, find_packages
except:
    from distutils.core import setup
from codecs import open
from os import path

#版本号
VERSION = '0.0.1'

#发布作者
AUTHOR = "liupeng"

#邮箱
AUTHOR_EMAIL = "lp3799@163.com"

#项目网址
URL = "https://github.com/vcancy/spider80s"

#项目名称
NAME = "lppypi"

#项目简介
DESCRIPTION = "lppypi"

#LONG_DESCRIPTION为项目详细介绍，这里取README.md作为介绍
here = path.abspath(path.dirname(__file__))
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    LONG_DESCRIPTION = f.read()

#搜索关键词
KEYWORDS = "lppypi"

#发布LICENSE
LICENSE = "MIT"

#包
PACKAGES = ["lppypi"]

#具体的设置
setup(
    name=NAME,
    version=VERSION,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
	long_description_content_type="text/markdown",
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',

    ],
    #指定控制台命令
    entry_points={
        'console_scripts': [
            'lppypi = lppypi:main',#pip安装完成后可使用lppypi命令调用lppypi下的main方法
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