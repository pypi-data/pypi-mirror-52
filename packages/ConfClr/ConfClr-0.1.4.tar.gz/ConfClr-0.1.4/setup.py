import re
import sys
from os.path import abspath, dirname, join
from setuptools import setup

MOD='ConfClr'


setup(
    name='ConfClr',
	version='0.1.4',
	description='Conformal Prediction Framework for Binary Classification',
    author='Rahul Vishwakarma',
    author_email='vishwr7@gmail.com',
    packages=[MOD],
	long_description=open('README.txt').read()
)
