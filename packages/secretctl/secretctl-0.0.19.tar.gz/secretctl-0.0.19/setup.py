import os
from setuptools import setup, find_packages
from _version import __version__

with open("README.md", "r") as fh:
    long_description = fh.read()

requirements=[
    'invoke==1.3.0',
    'boto3==1.9.226',
    'pyyaml==5.1.2',
    'requests==2.22.0',
    'colorama==0.4.1'
]

setup(
    name="secretctl",
    author="Nic Cheneweth",
    author_email="nic.cheneweth@thoughtworks.com",
    description="Command line tool for working with aws secrets manager",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ncheneweth/secretctl",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX :: Linux",
        'Development Status :: 3 - Alpha',
    ],
    python_requires='>=3.5',
    version=__version__,
    install_requires=requirements,
    setup_requires=['pytest-runner'],
    tests_require=['pytest'],
    entry_points={
        'console_scripts': ['secretctl = secretctl.main:program.run']
    }
)
