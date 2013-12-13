from ulib import validatorlib

from .. import tools
import ulib.tools.pep8 # pylint: disable=W0611


##### Public methods #####
def validUserName(arg) :
    return validatorlib.checkRegexp(arg, r"^[a-z_][a-z0-9_-]*$", "UNIX username")

def validGroupName(arg) :
    return validatorlib.checkRegexp(arg, r"^[a-z_][a-z0-9_-]*$", "UNIX groupname")


##### PEP8 #####
tools.pep8.setupAliases()

