import re

from . import tools
import ulib.tools.pep8 # pylint: disable=W0611


##### Exceptions #####
class ValidatorError(Exception) :
    pass


##### Public methods #####
def raiseError(arg, name) :
    raise ValidatorError("The argument \"%s\" is not a valid %s" % (arg, name))

def notEmptyStrip(arg, name) :
    if arg is None :
        raise ValidatorError("The empty argument is not a valid %s" % (name))
    return str(arg).strip()


###
def checkChain(arg, validators_list, name) :
    for validator in validators_list :
        try :
            return validator(arg)
        except Exception :
            pass
    raiseError(arg, name)

def checkRegexp(arg, regexp, name, limit = None) :
    arg = notEmptyStrip(arg, name)
    if not limit is None :
        arg = arg[:limit]
    if re.match(regexp, arg) is None :
        raiseError(arg, name)
    return arg

def checkRange(arg, valid_args_list, name) :
    if not arg in valid_args_list :
        raiseError(arg, name)
    return arg

def checkIterable(arg, item_validator, iterable_validator, pass_none_flag = False) :
    if arg is None :
        return ( None if pass_none_flag else item_validator(arg) )
    return list(map(item_validator, iterable_validator(arg)))


##### PEP8 #####
tools.pep8.setupAliases()

