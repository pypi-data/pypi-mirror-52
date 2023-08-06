#!/usr/bin/env python3

from setuptools import setup, find_packages


with open('README.md') as f:
    readme = f.read()

with open('LICENSE.txt') as f:
    license = f.read()

setup(
    name='hyperscalar',
    version='0.0.1',
    description='Next generation type',
    keywords=['hyperscalar'],
    url='https://github.com/fpgaco/hyperscalar',
    license=license,
    long_description=readme,
    author='Kenso Trabing',
    author_email='ktrabing@acm.org',
    maintainer='Kenso Trabing',
    maintainer_email='ktrabing@acm.org',
    packages=find_packages(exclude=('tests', 'docs')),
    classifiers=[
         'Programming Language :: Python :: 3.5',
         'License :: OSI Approved :: Apache Software License',
         'Operating System :: OS Independent',
         'Development Status :: 3 - Alpha',
         'Topic :: Scientific/Engineering :: Electronic Design Automation (EDA)'
     ]
)
