# -*- coding: utf-8 -*-
import os
from setuptools import setup, find_packages

try:  # for pip >= 10
    from pip._internal.req import parse_requirements
    from pip._internal.download import PipSession
except ImportError:  # for pip <= 9.0.3
    from pip.req import parse_requirements
    from pip.download import PipSession

requirements = parse_requirements(os.path.join(os.path.dirname(__file__), 'requirements.txt'), session=PipSession())

with open('README.rst') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='pyred',
    version='0.3.3',
    description='Easily send data to Amazon Redshift',
    long_description=readme,
    author='Dacker',
    author_email='hello@dacker.co',
    url='https://github.com/dacker-team/pyred',
    keywords='send data amazon redshift easy',
    packages=find_packages(exclude=('tests', 'docs')),
    license=license,
    python_requires='>=3',
    install_requires=[
        "psycopg2-binary>=2.7.4"
        "pandas>=0.25.0",
        "dbstream>=0.0.6"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
