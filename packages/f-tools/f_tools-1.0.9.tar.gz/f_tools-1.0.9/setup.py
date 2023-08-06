"""Setup for the f_tools package."""

import setuptools


with open('README.md') as f:
	README = f.read()

setuptools.setup(
	author="Filipe Ferreira",
	author_email="py@filipeandre.com",
	name='f_tools',
	license="MIT",
	description='A set of low level framework utilities',
	version='1.0.9',
	long_description=README,
	url='https://github.com/filipeandre/f_tools',
	packages=setuptools.find_packages(),
	python_requires=">=3.7",
	install_requires=[],
	classifiers=[
		'Development Status :: 5 - Production/Stable',
		'License :: OSI Approved :: MIT License',
		'Programming Language :: Python',
		'Programming Language :: Python :: 3.7',
		'Programming Language :: Python :: 3 :: Only',
		'Topic :: Software Development :: Libraries',
		'Topic :: Software Development :: Libraries :: Python Modules',
		'Intended Audience :: Developers',
		'Typing :: Typed'
	],
)