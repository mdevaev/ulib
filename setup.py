#!/usr/bin/env python2
# -*- coding: utf-8 -*-


from setuptools import setup


setup(
	name="helib",
	version="0.1",
	url="https://github.com/mdevaev/helib",
	license="GPLv3",
	author="Devaev Maxim",
	author_email="mdevaev@gmail.com",
	description="Useful python library",
	platforms="any",
	packages=[
		"helib",
		"helib/tools",
        "helib/validators",
	],
	classifiers=[
		"Topic :: Software Development :: Libraries :: Python Modules",
        "Development Status :: 4 - Beta"
		"Programming Language :: Python",
		"Operating System :: OS Independent",
	],
)

