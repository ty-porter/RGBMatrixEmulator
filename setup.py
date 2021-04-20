#!/usr/bin/env python

from distutils.core import setup
import codecs
import sys
import os.path as path

# where this file is located
cwd = path.dirname(__file__)

# get full description from rst file
longdesc = codecs.open(path.join(cwd, 'description.rst'), 'r', 'ascii').read()

version = '0.0.0'
# read version file to get version
with codecs.open(path.join(cwd, 'matrix_emulator/version.py'), 'r', 'ascii') as f:
    exec(f.read())
    version = __version__
# make sure version is not default
# make sure file reading worked
assert version != '0.0.0'

# download link based off tagged releases
download_link = 'https://github.com/zachpanz88/mlbgame/archive/v{}.zip'.format(
    version)

# setup options
setup(
    name='matrix_emulator',
    author='Tyler Porter',
    author_email='tyler.b.porter@gmail.com',
    version=version,
    license='MIT',
    description='A PC emulator for Raspberry Pi LED matrices driven by rpi-rgb-led-matrix',
    long_description=longdesc,
    url='https://github.com/zachpanz88/mlbgame',
    download_url=download_link,
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Development Status :: 5 - Production/Stable',
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
    packages=['matrix_emulator'],
    data_files=[('docs', ['README.md', 'LICENSE', 'description.rst'])],
    install_requires=['pygame'],
    extras_require={}
)