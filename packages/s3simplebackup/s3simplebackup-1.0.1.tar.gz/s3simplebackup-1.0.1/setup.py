#!/bin/env/python3

from setuptools import setup, find_packages

with open('README.rst', encoding='UTF-8') as f:
    readme = f.read()

setup(
    name='s3simplebackup',
    version='1.0.1',
    description='Backs up a file or directory to S3',
    long_description=readme,
    author='Ben Gardner',
    author_email='bgardner160@gmail.com',
    url='https://github.com/aDrongo/s3simplebackup/',
    download_url='https://github.com/aDrongo/s3simplebackup/archive/1.tar.gz',
    install_requires=['boto3'],
    packages=find_packages('src'),
    package_dir={'': 'src'},
    entry_points={
        'console_scripts': [
            's3simplebackup=s3simplebackup.cli:main',
            ]
        }
)
