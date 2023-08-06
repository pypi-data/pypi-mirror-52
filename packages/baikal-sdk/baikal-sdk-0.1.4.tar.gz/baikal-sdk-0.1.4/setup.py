#!/usr/bin/python
#
import os
from setuptools import setup

with open(os.path.join(os.getcwd(), "requirements.txt")) as req_file:
    requirements = req_file.read().splitlines()

with open(os.path.join(os.getcwd(), 'README.md')) as readme:
    long_description = readme.read()

setup(
    name='baikal-sdk',
    version='0.1.4',
    license='Apache 2.0',
    maintainer='4th Platform team',
    maintainer_email='4pf@telefonica.com',
    url='https://github.com/Telefonica/baikal-sdk/python',
    packages=['clients'],
    description='SDK to generate tokens for the 4th Platform',
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        'Programming Language :: Python :: 3.7',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Topic :: Security',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
    data_files=[('', ['LICENSE', 'NOTICE', 'README.md', 'requirements.txt'])],
    install_requires=requirements,
    zip_safe=False
)
