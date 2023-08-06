"""setup.py for python-xin package
"""
from datetime import date
from setuptools import setup, find_packages
from xin import __license__, __author__, __author_email__

with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name='xin',
    author=__author__,
    author_email=__author_email__,
    description='xin Python Library',
    long_description=long_description,
    keywords='python3 implementations',
    license=__license__,
    packages=find_packages(exclude=['test']),
    platforms='cross-platform',
    python_requires='>=3.7',
    url="https://git.haoohaoo.com/zhaoxin/python-xin",
    version=date.today().strftime(r'%Y.%m.%d'),
    install_requires=[
        'click>=7.0',
        'colorama>=0.4.1',
        'requests>=2.22.0',
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Natural Language :: Chinese (Simplified)',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: Implementation',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
    entry_points={
        'console_scripts': [
            'xin=xin.cli:xin'
        ],
    }
)
