import xmlrpc.client
import http.client
import socket

from .. import tools
import ulib.tools.pep8 # pylint: disable=W0611


##### Public constants #####
EXTRA_RESPONSE = "response"
EXTRA_HEADERS  = "headers"


##### Public classes #####
class ExtraTransport(xmlrpc.client.Transport) :
    def __init__(self, *args_tuple, **kwargs_dict) :
        self.user_agent = kwargs_dict.pop("user_agent", self.user_agent)
        self._timeout = kwargs_dict.pop("timeout", socket.getdefaulttimeout())
        self._extra_flag = kwargs_dict.pop("extra_flag", False)
        xmlrpc.client.Transport.__init__(self, *args_tuple, **kwargs_dict)

    def make_connection(self, host_name) :
        return _TimeoutedConnection(host_name, timeout=self._timeout)

    def parse_response(self, response) :
        assert hasattr(response, "getheaders"), "This transport supports only the HTTP(S) protocol"
        retval = xmlrpc.client.Transport.parse_response(self, response)
        headers_dict = dict(response.getheaders())

        if not self._extra_flag :
            return retval
        else :
            # XXX: This magic I found in /usr/lib/python3.3/xmlrpc/client.py:1422
            # ServerProxy code will be executed only for a dictionary with a single element,
            # inevitably leads to an error (you can not index the dictionary).
            # Since we have a few items, then everything will work fine.
            # However, this behavior can be used to change, so in this case I have a test.
            if len(retval) == 1 :
                retval = retval[0]
            return {
                EXTRA_RESPONSE : retval,
                EXTRA_HEADERS  : headers_dict,
            }


##### Private classes #####
class _TimeoutedConnection(http.client.HTTPConnection) :
    def connect(self):
        http.client.HTTPConnection.connect(self)
        self.sock.settimeout(self.timeout)


##### PEP8 #####
tools.pep8.setupAliases()

