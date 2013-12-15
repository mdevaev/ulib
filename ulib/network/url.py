import urllib.request
import urllib.parse
import urllib.error
import http.client
import socket
try :
    import socks
except ImportError :
    socks = None # pylint: disable=C0103

from .. import tools
import ulib.tools.pep8 # pylint: disable=W0611


##### Exceptions #####
class ServerError(Exception) :
    def __init__(self, code, text) :
        super(ServerError, self).__init__()
        self._code = code
        self._text = text
        self._message = http.client.responses[code]

    def code(self) :
        return self._code

    def message(self) :
        return self._message

    def info(self) :
        return "%d %s" % (self._code, self._message)

    def text(self) :
        return self._text

    def __str__(self) :
        return "%d %s [%s]" % (self._code, self._message, self._text)


##### Public classes #####
class SocksHandler(urllib.request.HTTPHandler) :
    def __init__(self, *args_tuple, **kwargs_dict) :
        urllib.request.HTTPHandler.__init__(self, debuglevel=kwargs_dict.pop("debuglevel", 0))
        self._args_tuple = args_tuple
        self._kwargs_dict = kwargs_dict

    def http_open(self, request) :
        def build(host, port = None, strict = None, timeout = socket._GLOBAL_DEFAULT_TIMEOUT) : # pylint: disable=W0212
            return SocksConnection(*self._args_tuple, host=host, port=port, strict=strict, timeout=timeout, **self._kwargs_dict)
        return self.do_open(build, request)

class SocksConnection(http.client.HTTPConnection) :
    def __init__(self, proxy_url = None, proxy_type = None, proxy_host = None, proxy_port = None,
        proxy_user = None, proxy_passwd = None, rdns_flag = True, *args_tuple, **kwargs_dict) :
        if socks is None :
            raise RuntimeError("Required module SocksiPy")
        http.client.HTTPConnection.__init__(self, *args_tuple, **kwargs_dict)

        if not proxy_url is None :
            parsed = urllib.parse.urlparse(proxy_url)
            scheme = parsed.scheme
            proxy_user = parsed.username
            proxy_passwd = parsed.password
            proxy_host = parsed.hostname
            proxy_port = ( parsed.port or 1080 )
            proxy_type = {
                "socks4" : socks.PROXY_TYPE_SOCKS4,
                "socks5" : socks.PROXY_TYPE_SOCKS5,
            }.get(( scheme or "" ).lower())
            if proxy_type is None :
                raise RuntimeError("Invalid SOCKS protocol: %s" % (scheme))

        self._proxy_args_tuple = (proxy_type, proxy_host, proxy_port, rdns_flag, proxy_user, proxy_passwd)

    def connect(self) :
        self.sock = socks.socksocket()
        self.sock.setproxy(*self._proxy_args_tuple)
        if not self.timeout is socket._GLOBAL_DEFAULT_TIMEOUT : # pylint: disable=W0212
            self.sock.settimeout(self.timeout)
        self.sock.connect((self.host, self.port))


##### PEP8 #####
tools.pep8.setupAliases()

