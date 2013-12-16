import re

from .. import tools
import ulib.tools.pep8 # pylint: disable=W0611

from .. import validatorlib
from ..validatorlib import ValidatorError


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

    if min_value is not None and arg < min_value :
        raise ValidatorError("The argument \"%s\" must be greater or equal than %d" % (arg, min_value))
    if max_value is not None and arg > max_value :
        raise ValidatorError("The argument \"%s\" must be lesser or equal then %d" % (arg, max_value))
    return arg


###
def validRange(arg, valid_args_list) :
    return validatorlib.checkRange(arg, valid_args_list, "range %s" % (str(valid_args_list)))

def validStringList(arg) :
    if isinstance(arg, (list, tuple)) :
        return list(map(str, list(arg)))
    arg = validatorlib.notEmptyStrip(arg, "string list")
    return list(filter(None, re.split(r"[,\t ]+", arg)))


###
def validEmpty(arg) :
    if arg is None or (isinstance(arg, str) and len(arg.strip()) == 0) :
        return None
    else :
        return arg

def validMaybeEmpty(arg, validator) :
    arg = validEmpty(arg)
    if arg is not None :
        return validator(arg)
    else :
        return None


##### PEP8 #####
tools.pep8.setupAliases()

