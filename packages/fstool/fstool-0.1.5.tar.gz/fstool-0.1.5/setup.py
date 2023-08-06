from setuptools import setup, find_packages

import fstool

with open('README.md', 'r') as f:
    long_description = f.read()

setup(
    name='fstool',
    version=fstool.__version__,
    description='file system tool extension',
    long_description_content_type='text/markdown',
    author='mhaisham',
    author_email='mhaisham79@gmail.com',
    url='https://github.com/mHaisham/fstool',
    packages=find_packages(),
    python_requires='>=3.6'
)