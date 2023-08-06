"""main.py"""
from invoke import Collection, Program
from secretctl import cli
from _version import __version__

program = Program(namespace=Collection.from_module(cli), version=__version__)
