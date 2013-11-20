# -*- coding: utf-8 -*-


import unittest

from ulib import tools
import ulib.tools.url # pylint: disable=W0611


##### Public classes #####
class TestExceptions(unittest.TestCase) :
    def test_server_error(self) :
        try :
            raise tools.url.ServerError(404, "This file is not found")
        except tools.url.ServerError as err :
            self.assertEqual(err.code(), 404)
            self.assertEqual(err.message(), "Not Found")
            self.assertEqual(err.info(), "404 Not Found")
            self.assertEqual(err.text(), "This file is not found")

