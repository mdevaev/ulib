#!/usr/bin/env python2
# -*- coding: utf-8 -*-


from setuptools import setup


setup(
	name="ulib",
	version="0.1",
	url="https://github.com/mdevaev/ulib",
	license="GPLv3",
	author="Devaev Maxim",
	author_email="mdevaev@gmail.com",
	description="Useful python library",
	platforms="any",
	packages=[
		"ulib",
		"ulib/tools",
        "ulib/validators",
	],
	classifiers=[
		"Topic :: Software Development :: Libraries :: Python Modules",
        "Development Status :: 4 - Beta"
		"Programming Language :: Python",
		"Operating System :: OS Independent",
	],
)

