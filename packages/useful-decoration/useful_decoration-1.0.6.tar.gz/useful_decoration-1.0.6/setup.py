# -*- coding: utf-8 -*- 
"""
@User     : Frank
@File     : setup.py
@DateTime : 2019-09-16 11:24 
@Email    : frank.chang@lexisnexis.com
"""
from setuptools import setup

with open('README.md', 'r', encoding='UTF-8') as f:
    long_description = f.read()

setup(
    name="useful_decoration",
    license='Apache License 2.0',
    version='1.0.6',
    packages=['useful_decoration'],
    zip_safe=False,
    include_package_data=True,
    long_description=long_description,
    url='https://github.com/changyubiao',
    author='frank',
    author_email='frank.chang@lexisnexis.com',
    description='测试发布包功能',
    python_requires='>=3.6',

)

if __name__ == '__main__':
    pass
