# -*- coding: utf-8 -*-


import os

from helib.validatorlib import ValidatorError


##### Public methods #####
def validAccessiblePath(path, mode = os.F_OK) :
    if path is None :
        raise ValidatorError("Empty argument is not valid a path")
    path = os.path.normpath(str(path).strip())
    if not os.access(path, mode) :
        raise ValidatorError("Argument \"%s\" is not valid accessible path" % (path))
    return path

