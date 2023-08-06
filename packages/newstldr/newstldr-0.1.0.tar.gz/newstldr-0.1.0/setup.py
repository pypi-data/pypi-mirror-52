"""
Flasik
"""

import os
from setuptools import setup, find_packages

base_dir = os.path.dirname(__file__)


with open('requirements.txt') as f:
    install_requires = f.read().splitlines()

with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name="newstldr",
    version="0.1.0",
    license="MIT",
    author="Mardix",
    author_email="mcx2082@gmail.com",
    description="NewsTLDR",
    url="https://github.com/mardix/newstldr-service",
    long_description=long_description,
    long_description_content_type="text/markdown",
    py_modules=['newstldr'],
    include_package_data=True,
    packages=find_packages(exclude=["*.tests", "*.tests.*", "tests.*", "tests"]),
    install_requires=install_requires,
    keywords=[],
    platforms='any',
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
    zip_safe=False
)

