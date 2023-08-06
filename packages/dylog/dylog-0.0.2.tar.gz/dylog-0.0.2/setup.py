# -*- coding: utf-8 *-*
try:
    from setuptools import setup
except ImportError:
    from distutils import setup


long_description = open("README.rst").read()

setup(
    name='dylog',
    version='v0.0.2',
    description='Python centralized logging using DynamoDB',
    long_description=long_description,
    author='Victor M',
    author_email='viktor.manuel.garcia@gmail.com',
    maintainer='Victor M',
    maintainer_email="viktor.manuel.garcia@gmail.com",
    url='https://github.com/vgmartinez/dylog',
    download_url = 'https://github.com/vgmartinez/dylog/archive/v0.0.2.zip',
    packages=['dylog'],
    keywords=["dylog", "logging", "dynamo", "dynamodb"],
    install_requires=['boto3'],
    classifiers=[
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Topic :: System :: Logging",
        "Topic :: Database"],
)
