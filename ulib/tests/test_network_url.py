import unittest

from ulib import network
import ulib.network.url # pylint: disable=W0611


##### Public classes #####
class TestExceptions(unittest.TestCase) :
    def test_server_error(self) :
        try :
            raise network.url.ServerError(404, "This file is not found")
        except network.url.ServerError as err :
            self.assertEqual(err.code(), 404)
            self.assertEqual(err.message(), "Not Found")
            self.assertEqual(err.info(), "404 Not Found")
            self.assertEqual(err.text(), "This file is not found")

