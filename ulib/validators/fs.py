# -*- coding: utf-8 -*-


import os

from ulib import validatorlib


##### Public methods #####
def validAccessiblePath(path, mode = os.F_OK) :
    name = "accessible path"
    path = validatorlib.notEmptyStrip(path, name)
    if not os.access(path, mode) :
        validatorlib.raiseError(path, name)
    return path

def validFileName(arg) :
    # XXX: http://en.wikipedia.org/wiki/Filename#Comparison_of_filename_limitations
    if os.name != "posix" :
        raise NotImplementedError("This validator is not implemented for %s-class" % (os.name))

    name = "filename"
    arg = os.path.normpath(arg)
    if arg in (".", "..") :
        validatorlib.raiseError(arg, name)
    return validatorlib.checkRegexp(arg, r"^[^/\0]+$", name)

