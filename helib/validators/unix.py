# -*- coding: utf-8 -*-


from helib import validatorlib


##### Public methods #####
def validUserName(arg) :
    return validatorlib.checkRegexp(arg, r"^[a-z_][a-z0-9_-]*$", "UNIX username")

def validGroupName(arg) :
    return validatorlib.checkRegexp(arg, r"^[a-z_][a-z0-9_-]*$", "UNIX groupname")

