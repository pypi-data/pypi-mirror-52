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
    name='pyspreadsheet',
    version='0.1.0',
    description='Easily send data to Google Sheets',
    long_description=readme,
    author='Dacker',
    license=license,
    author_email='hello@dacker.co',
    url='https://github.com/dacker-team/pyspreadsheet',
    keywords='send data google spreadsheet sheets easy',
    packages=find_packages(exclude=('tests', 'docs')),
    python_requires='>=3',
    install_requires=[str(requirement.req) for requirement in requirements],
)
