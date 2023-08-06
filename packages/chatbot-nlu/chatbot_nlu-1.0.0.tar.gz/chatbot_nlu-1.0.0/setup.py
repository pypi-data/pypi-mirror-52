# -*- coding: utf-8 -*-

'''
@Author  :   Xu

@Software:   PyCharm

@File    :   set_up.py

@Time    :   2019-06-06 16:22

@Desc    :   setup

'''
from setuptools import find_packages, setup
import pathlib

# Package meta-data.
NAME = 'chatbot_nlu'
DESCRIPTION = 'nlu of augment、chatbot、classification and featureproject of chinese text'
URL = 'https://github.com/yongzhuo/nlp_xiaojiang'
EMAIL = 'charlesxu86@163.com'
AUTHOR = 'xu'
LICENSE = 'MIT'

HERE = pathlib.Path(__file__).parent
README = (HERE / "README.md").read_text()

required = [
            'scikit-learn>=0.19.1',
            'bert-serving-client==1.8.9',
            'bert-serving-server==1.9.2',
            'tensorflow-gpu==1.14.0',]

setup(name=NAME,
        version='1.0.0',
        description=DESCRIPTION,
        long_description=README,
        long_description_content_type="text/markdown",
        author=AUTHOR,
        author_email=EMAIL,
        url=URL,
        packages=find_packages(exclude=('tests')),
        install_requires=required,
        license=LICENSE,
        classifiers=['License :: OSI Approved :: MIT License',
                     'Programming Language :: Python :: 3.4',
                     'Programming Language :: Python :: 3.5',
                     'Programming Language :: Python :: 3.6',
                     'Programming Language :: Python :: 3.7',
                     'Programming Language :: Python :: 3.8',
                     'Programming Language :: Python :: Implementation :: CPython',
                     'Programming Language :: Python :: Implementation :: PyPy'],)
print("Welcome to Chatbot NLU")
