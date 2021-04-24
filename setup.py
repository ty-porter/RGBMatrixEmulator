#!/usr/bin/env python

from setuptools import find_packages, setup
import codecs
import sys
import os.path as path

cwd = path.dirname(__file__)

with open("description.md", "r") as fh:
    long_description = fh.read()

version = '0.0.0'
with codecs.open(path.join(cwd, 'RGBMatrixEmulator/version.py'), 'r', 'ascii') as f:
    exec(f.read())
    version = __version__
assert version != '0.0.0'

setup(
    name='RGBMatrixEmulator',
    author='Tyler Porter',
    author_email='tyler.b.porter@gmail.com',
    version=version,
    license='MIT',
    description='A PC emulator for Raspberry Pi LED matrices driven by rpi-rgb-led-matrix',
    long_description_content_type='text/markdown',
    long_description=long_description,
    url='https://github.com/ty-porter/RGBMatrixEmulator',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: Other Audience',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Natural Language :: English',
        'Topic :: Other/Nonlisted Topic',
    ],
    keywords=[
        'LED matrix',
        'matrix',
        'raspberry pi',
        'raspberry',
        'RPI',
        'LED'
    ],
    platforms='ANY',
    packages=find_packages(),
    data_files=[
        ('docs', ['README.md', 'LICENSE', 'description.md']),
        ('RGBMatrixEmulator', ['RGBMatrixEmulator/icon.png'])
    ],
    install_requires=[
        'bdfparser<=2.2.0',
        'pygame<=1.9.6',
        'scikit-image<=0.18.1'
    ],
    include_package_data=True
)