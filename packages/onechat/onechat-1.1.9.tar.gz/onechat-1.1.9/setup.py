#!/usr/bin/env python
import os
from distutils.core import setup
def read(*paths):
    with open(os.path.join(*paths), 'r') as f:
        return f.read()
setup(
	name='onechat',
	version='1.1.9',
	packages=['onechat'],
	url='https://chat-develop.one.th',
	license='MIT',
	author='Punnawish.th',
	author_email='punnawish.th@inet.co.th',
	keywords = "onechat",
	description='onechat',
	long_description=(read('README.md')),
	classifiers= [
		'Development Status :: 5 - Production/Stable',
		'Intended Audience :: Developers',
		'Natural Language :: English',
		'License :: OSI Approved :: MIT License',
		'Operating System :: OS Independent',
		'Programming Language :: Python',
		'Programming Language :: Python :: 2',
		'Programming Language :: Python :: 3',
		'Programming Language :: Python :: Implementation :: CPython',
		'Programming Language :: Python :: Implementation :: IronPython',
		'Programming Language :: Python :: Implementation :: Jython',
		'Programming Language :: Python :: Implementation :: PyPy',
		'Topic :: Scientific/Engineering'
	],
)
