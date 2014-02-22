from .. import tools
import ulib.tools.pep8 # pylint: disable=W0611

from .. import validatorlib


##### Public methods #####
def validObjectName(arg) :
	return validatorlib.checkRegexp(arg,
		r"^[a-zA-Z_][a-zA-Z0-9_]*$",
		"Python object name",
	)


##### PEP8 #####
tools.pep8.setupAliases()

