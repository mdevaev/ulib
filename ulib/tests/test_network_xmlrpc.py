import unittest
import xmlrpc.client
import socket

from .. import tools
import ulib.tools.pep8 # pylint: disable=W0611

from .. import network
import ulib.network.xmlrpc


##### Public classes #####
class TestExtraTransport(unittest.TestCase) :
    def setUp(self) :
        self._usually = self._makeProxy()
        self._timeouted = self._makeProxy(timeout=10)
        self._timeout_failed = self._makeProxy(timeout=0.001)
        self._extra = self._makeProxy(extra_flag=True)


    ### Tests ###

    def test_usually(self) :
        self.assertEqual(self._usually.examples.getStateName(1), "Alabama")

    def test_timeouted(self) :
        self.assertEqual(self._timeouted.examples.getStateName(1), "Alabama")

    def test_timeout_failed(self) :
        self.assertRaises(socket.timeout, self._timeout_failed.examples.getStateName, (1,))

    def test_extra(self) :
        result_dict = self._extra.examples.getStateName(1)
        self.assertEqual(result_dict[network.xmlrpc.EXTRA_RESPONSE], "Alabama")
        self.assertEqual(result_dict[network.xmlrpc.EXTRA_HEADERS]["X-Powered-By"], "ASP.NET")


    ### Private ###

    def _makeProxy(self, **kwargs_dict) :
        return xmlrpc.client.ServerProxy(
            "http://www.cookcomputing.com/xmlrpcsamples/RPC2.ashx",
            transport=network.xmlrpc.ExtraTransport(**kwargs_dict)
        )


##### PEP8 #####
tools.pep8.setupAliases()

