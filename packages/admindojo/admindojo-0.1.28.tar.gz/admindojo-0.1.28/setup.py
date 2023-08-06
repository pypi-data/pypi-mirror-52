#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup, find_packages

with open('README.md') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = ['Click>=6.0', 'termcolor', 'click-default-group']

setup_requirements = ['pytest-runner', ]

test_requirements = ['pytest', ]

setup(
    author="Marvin Heimbrodt",
    author_email='marvin@6uhrmittag.de',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    description="The admindojo client for VMs",
    entry_points={
        'console_scripts': [
            'admindojo=admindojo.cli:cli',
        ],
    },
    install_requires=requirements,
    license="MIT license",
    long_description_content_type='text/markdown',
    long_description=readme,
    include_package_data=True,
    keywords='admindojo',
    name='admindojo',
    packages=find_packages(include=['admindojo']),
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/admindojo/admindojo-client',
    version='0.1.28',
    zip_safe=False,
)
