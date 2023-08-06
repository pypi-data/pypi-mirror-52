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

with open('README.md', 'r') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='pyganalytics',
    version='0.1.0',
    description='Easily get data from Google Analytics',
    long_description=readme,
    long_description_content_type="text/markdown",
    author='Dacker',
    author_email='hello@dacker.co',
    url='https://github.com/dacker-team/pyganalytics',
    license=license,
    keywords='get data google analytics easy',
    packages=find_packages(exclude=('tests', 'docs')),
    python_requires='>=3',
    install_requires=[str(requirement.req) for requirement in requirements],
)
