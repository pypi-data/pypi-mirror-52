# coding: utf-8

from setuptools import setup

setup(
    name='bs-test', 
    version='0.0.4', # 项目版本 
    author='bunshinn', # 项目作者 
    author_email='bunshinn@163.com', # 作者email 
    url='https://github.com/bunshinn/bstools', # 项目代码仓库
    description='test', # 项目描述 
    packages=['bstest'], # 包名 
    install_requires=[],
    entry_points={
        'console_scripts': [
            'get_time=get_time:get_time', # 使用者使用get_time时,就睡到get_time项目下的__init__.py下执行get_time函数
            'get_timestamp=get_time:get_timestamp',
        ]
    } 
)
