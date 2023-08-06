#!/usr/bin/env python
# -*- coding: utf-8 -*-

import subprocess
import os
from setuptools import setup, find_packages
from setuptools.command.develop import develop
from setuptools.command.install import install


# Dynamically compile protos
def compileProtoBuf():
    res = subprocess.call(['bash', './compile.sh'])
    assert res == 0, 'cannot compile protobuf'


class PostDevelopCommand(develop):
    """Post-installation for development mode."""
    def run(self):
        compileProtoBuf()
        develop.run(self)


class PostInstallCommand(install):
    """Post-installation for installation mode."""
    def run(self):
        compileProtoBuf()
        import os
        os.system("pip install protobuf numpy six")
        install.run(self)


with open('HISTORY.rst') as history_file:
    history = history_file.read()

preparing_PyPI_package = False
version = '0.3.6'

if not preparing_PyPI_package:
    with open('tb_paddle/__init__.py', 'a') as f:
        f.write('\n__version__ = "{}"\n'.format(version))

requirements = [
    'numpy',
    'protobuf >= 3.6.1',
    'six',
    'pillow',
    'moviepy',
]

setup(
    name='tb-paddle',
    version=version,
    description='tb-paddle is a toolkit to visualize Paddle logged data in TensorBoard.',
    long_description=history,
    author='ShuLiang Lin',
    author_email='',
    url='https://github.com/linshuliang/tb-paddle',
    packages=['tb_paddle'],
    include_package_data=True,
    install_requires=requirements,
    license='MIT license',
    zip_safe=False,
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    cmdclass={
        'develop': PostDevelopCommand,
        'install': PostInstallCommand,
    },
)
