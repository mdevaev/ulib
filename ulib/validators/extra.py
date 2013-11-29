import re
import json

from ulib import validatorlib
from ulib.validatorlib import ValidatorError


##### Public methods #####
def validJson(arg) :
    arg = validatorlib.notEmptyStrip(arg, "JSON structure")
    try :
        return json.dumps(json.loads(arg))
    except Exception as err :
        raise ValidatorError("The argument \"%s\" is not a valid JSON structure: %s" % (arg, str(err)))

def validHexString(arg) :
    return validatorlib.checkRegexp(arg, r"^[0-9a-fA-F]+$", "hex string")

def validUuid(arg):
    return validatorlib.checkRegexp(arg, r"^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$", "UUID string")

