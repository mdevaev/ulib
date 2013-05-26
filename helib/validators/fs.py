# -*- coding: utf-8 -*-


import os

from helib import validatorlib
from helib.validatorlib import ValidatorError


##### Public methods #####
def validAccessiblePath(path, mode = os.F_OK) :
    name = "accessible path"
    path = validatorlib.notEmptyStrip(path, name)
    if not os.access(path, mode) :
        validatorlib.raiseError(path, name)
    return path

