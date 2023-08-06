#!/usr/bin/env python

from setuptools import find_packages, setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='ndvector',
    version='1.1.0',
    author='Tom Egan',
    author_email='tkegan@greenneondesign.com',
    license='Apache License 2.0',
    description='A library for vector math in n dimensions.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/tkegan/ndvector',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
    ],
    keywords=[
        'vector', 'math', 'linear algebra'
    ],
    python_requires='>=3.5',
)