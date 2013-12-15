import unittest
import urllib.request

from .. import tools
import ulib.tools.pep8 # pylint: disable=W0611

from .. import network
import ulib.network.url


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

class TestGzipHandler(unittest.TestCase) :
    def test_yandex_gzip(self) :
        opener = urllib.request.build_opener(network.url.GzipHandler(only_gzip_flag=True))
        request = urllib.request.Request("http://yandex.ru", headers={ "Accept-Encoding" : "gzip" })
        self.assertTrue(opener.open(request).read().startswith(b"<!DOCTYPE html>"), "Garbage?")


##### PEP8 #####
tools.pep8.setupAliases()

