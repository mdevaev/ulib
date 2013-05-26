# -*- coding: utf-8 -*-


import re
import cjson

from helib import tools
import helib.tools.coding # pylint: disable=W0611

from helib import validatorlib
from helib.validatorlib import ValidatorError


##### Public methods #####
def validBool(arg) :
    true_args_list = ("1", "true", "yes")
    false_args_list = ("0", "false", "no")
    name = "bool (%s or %s)" % (str(true_args_list), str(false_args_list))
    arg = validatorlib.notEmptyStrip(arg, name).lower()
    arg = validatorlib.checkRange(arg, true_args_list + false_args_list, name)
    return ( arg in true_args_list )

def validNumber(arg, min_value = None, max_value = None, value_type = int) :
    arg = validatorlib.notEmptyStrip(arg, "number")
    try :
        arg = value_type(arg)
    except Exception :
        validatorlib.raiseError(arg, "number")

    if not min_value is None and arg < min_value :
        raise ValidatorError("The argument \"%s\" must be greater or equal than %d" % (tools.coding.utf8(arg), min_value))
    if not max_value is None and arg > max_value :
        raise ValidatorError("The argument \"%s\" must be lesser or equal then %d" % (tools.coding.utf8(arg), max_value))
    return arg


###
def validRange(arg, valid_args_list) :
    return validatorlib.checkRange(arg, valid_args_list, "range %s" % (str(valid_args_list)))

def validStringList(arg) :
    if isinstance(arg, (list, tuple)) :
        return map(str, list(arg))
    arg = validatorlib.notEmptyStrip(arg, "string list")
    return filter(None, re.split(r"[,\t ]+", arg))


###
def validEmpty(arg) :
    if arg is None or (isinstance(arg, (str, unicode)) and len(arg.strip()) == 0) :
        return None
    else :
        return arg

def validMaybeEmpty(arg, validator) :
    arg = validEmpty(arg)
    if not arg is None :
        return validator(arg)
    else :
        return None

###
def validJson(arg) :
    arg = validatorlib.notEmptyStrip(arg, "JSON structure")
    try :
        return cjson.encode(cjson.decode(arg))
    except Exception, err :
        raise ValidatorError("The argument \"%s\" is not a valid JSON structure: %s" % (tools.coding.utf8(arg), str(err)))

def validHexString(arg) :
    return validatorlib.checkRegexp(arg, r"^[0-9a-fA-F]+$", "hex string")

