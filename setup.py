#!/usr/bin/env python2
# -*- coding: utf-8 -*-


from ulib import const

from setuptools import setup


##### Main #####
if __name__ == "__main__" :
    setup(
        name="ulib",
        version=const.VERSION,
        url=const.UPSTREAM_URL,
        license="GPLv3",
        author="Devaev Maxim",
        author_email="mdevaev@gmail.com",
        description="Useful python library",
        platforms="any",

        packages=(
            "ulib",
            "ulib/tools",
            "ulib/validators",
        ),

        classifiers=(
            "Topic :: Software Development :: Libraries :: Python Modules",
            "Development Status :: 4 - Beta",
            "Programming Language :: Python",
            "Operating System :: OS Independent",
        ),
    )

