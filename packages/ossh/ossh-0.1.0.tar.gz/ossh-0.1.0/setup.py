from setuptools import setup, find_packages
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()


setup(
    name='ossh',
    version='0.1.0',  # Required
    description='A ssh cli tool to make your ssh easy',
    url='https://github.com/wangzewang/oak-ssh',
    author='wangzewang',
    author_email='wangzewang@outlook.com',

    # For a list of valid classifiers, see https://pypi.org/classifiers/
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],

    keywords='ssh cli tool',
    packages=find_packages(exclude=['contrib', 'docs', 'tests']),
    python_requires='>=3.5',
    entry_points={
        'console_scripts': [
            'ossh=ossh:main',
        ],
    },
    project_urls={
        'Bug Reports': 'https://github.com/wangzewang/oak-ssh/issues',
        'Say Thanks!': 'http://saythanks.io/to/wangzewang',
        'Source': 'https://github.com/wangzewang/oak-ssh/',
    },
)
