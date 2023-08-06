#!/usr/bin/env python
import setuptools
from setuptools import setup

setup(
    name='pubopinion',
    version='0.1.0a3',
    description='public opinion module',
    url='https://gitlab.com/dzywork/cadrem-pubopinion-crawler.git',
    author='戴志勇',
    author_email='dzywork@Outlook.com',
    license='MIT',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    keywords='crawler scrapy python',
    packages=setuptools.find_packages(),
    python_requires='>=3.6',
)