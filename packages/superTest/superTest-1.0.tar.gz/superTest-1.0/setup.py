#coding=utf-8
from distutils.core import setup
# or
# from distutils.core import setup

setup(
        name='superTest',     # 包名字
        version='1.0',   # 包版本
        description='This is a test of the setup',   # 简单描述
        author='dumin',  # 作者
        author_email='dumin189@163.com',  # 作者邮箱    # 包的主页
        py_modules=['superTest.demo1','superTest.demo2']                # 包
)