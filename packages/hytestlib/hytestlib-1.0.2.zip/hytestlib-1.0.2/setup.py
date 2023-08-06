# 有两种打包方式

# 不会自动打包 README.rst 文件
# from distutils.core import setup

# 会自动打包 README.rst 文件
from setuptools import setup

# 会包含setup.py文件
# python setup.py sdist

# 二进制打包,不会包含setup.py文件,是特定平台和Python平台的一个存档
# python setup.py bdist

def readme_file():
    with open("README.rst", encoding="utf-8") as rf:
        return rf.read()


setup(name="hytestlib", version="1.0.2", description="this is a great lib,too",
      packages=["hytestlib"], py_modules=["Tool"], author="Hy", author_email="843923647@qq.com",
      long_description=readme_file(), license="MIT", url="https://github.com/hy/Python_code")
