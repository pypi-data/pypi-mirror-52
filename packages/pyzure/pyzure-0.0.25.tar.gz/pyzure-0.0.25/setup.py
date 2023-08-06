# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

try:  # for pip >= 10
    from pip._internal.req import parse_requirements
except ImportError:  # for pip <= 9.0.3
    from pip.req import parse_requirements

reqs = parse_requirements("requirements.txt", session='hack')
reqs = [str(ir.req) for ir in reqs]

with open('README.rst') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='pyzure',
    version='0.0.25',
    description='Easily send data to Microsoft Azure SQL DB',
    long_description=readme,
    author='Dacker',
    author_email='hello@dacker.co',
    url='https://github.com/dacker-team/pyzure',
    keywords='send data microsoft azure sql db easy',
    packages=find_packages(exclude=('tests', 'docs')),
    python_requires='>=3',
    install_requires=reqs,
)
