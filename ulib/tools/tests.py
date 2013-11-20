import unittest

from ulib.validatorlib import ValidatorError


##### Public classes #####
class TestValidatorsCase(unittest.TestCase) :
    def checkValidator(self, validator, valids_list, invalids_list) :
        for (valid, result) in valids_list :
            self.assertEqual(validator(valid), result)
        for invalid in invalids_list :
            self.assertValidatorError(validator, invalid)

    def assertValidatorError(self, validator, arg) :
        try :
            validator(arg)
            raise AssertionError("Validator should not miss the value of \"%s\"" % (arg))
        except ValidatorError : pass

