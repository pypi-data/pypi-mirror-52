#!/usr/bin/env python
# -*- coding: utf-8 -*-
from setuptools import (
    setup,
    find_packages,
)

extras_require = {
    'test': [
        "cytoolz>=0.9.0,<1.0.0",
        "pytest==4.0.2",
        "pytest-timeout==1.3.3",
        "pytest-xdist==1.25.0",
        "tox>=2.9.1,<3",
    ],
    'test-asyncio': [
        "pytest-asyncio==0.9.0",
    ],
    'test-trio': [
        "pytest-trio==0.5.2",
    ],
    'lint': [
        "black==19.3b",
        "flake8==3.7.7",
        "isort==4.3.18",
        "mypy==0.701",
    ],
    'doc': [
        "Sphinx>=1.6.5,<2",
        "sphinx_rtd_theme>=0.1.9",
        "towncrier>=19.2.0, <20",
    ],
    'dev': [
        "bumpversion>=0.5.3,<1",
        "pytest-watch>=4.1.0,<5",
        "wheel",
        "twine",
        "ipython",
    ],
    'snappy': [
        "python-snappy>=0.5.3,<1"
    ]
}


extras_require['dev'].extend(extras_require['test'])
extras_require['dev'].extend(extras_require['lint'])
extras_require['dev'].extend(extras_require['doc'])

with open('./README.md') as readme:
    long_description = readme.read()

setup(
    name='lahja',
    # *IMPORTANT*: Don't manually change the version here. Use `make bump`, as described in readme
    version='0.14.5',
    description="Generic event bus for asynchronous cross-process communication",
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='The Lahja developers',
    author_email='christoph.burgdorf@gmail.com',
    url='https://github.com/ethereum/lahja',
    include_package_data=True,
    install_requires=[
        "async-generator>=1.10,<2",
        "trio>=0.11,<0.12",
        "trio_typing>=0.2.0,<0.3.0",
    ],
    python_requires='>=3.6, <4',
    extras_require=extras_require,
    py_modules=['lahja'],
    license="MIT",
    zip_safe=False,
    keywords='eventbus asyncio trio',
    packages=find_packages(exclude=["tests", "tests.*"]),
    package_data={'lahja': ['py.typed']},
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: Implementation :: PyPy',
    ],
)
