#!/usr/bin/env python

from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

install_requires = [
    'requests==2.21.0',
    'python-dateutil==2.8.0',
    'numpy',
]

tests_require = [
    'pytest',
    ]

setup(
    name='dl_analytics',
    version='0.0.4',
    author='Zhi Rui Tam',
    author_email='ray@currentsapi.services',
    license='MIT',
    url='https://github.com/theblackcat102/dl_analytics',
    packages=find_packages(),
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=install_requires,
    tests_require=tests_require,
    description='Client to send stats to server',
    download_url='https://github.com/currentsapi-dev/currentsapi-python/archive/master.zip',
    keywords=['tools', 'wrapper'],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
)