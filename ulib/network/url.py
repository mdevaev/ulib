import urllib.request
import urllib.parse
import urllib.error
import http.client
import socket
import gzip
try :
    import socks
except ImportError :
    socks = None # pylint: disable=C0103

from .. import tools
import ulib.tools.pep8 # pylint: disable=W0611


##### Public constants #####
SCHEME_SOCKS4 = "socks4"
SCHEME_SOCKS5 = "socks5"

SCHEME_TO_TYPE_MAP = {}
if socks is not None :
    SCHEME_TO_TYPE_MAP.update({
            SCHEME_SOCKS4 : socks.PROXY_TYPE_SOCKS4,
            SCHEME_SOCKS5 : socks.PROXY_TYPE_SOCKS5,
        })

SOCKS_PORT = 1080


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
class GzipHandler(urllib.request.HTTPHandler) :
    def __init__(self, debuglevel = 0, only_gzip_flag = False) :
        self._only_gzip_flag = only_gzip_flag
        urllib.request.HTTPHandler.__init__(self, debuglevel=debuglevel)

    def http_request(self, request) :
        request.add_header("Accept-Encoding", "gzip")
        return request

    def http_response(self, request, response) :
        if response.headers.get("content-encoding") == "gzip" :
            gzip_file = gzip.GzipFile(fileobj=response, mode="r")
            old_response = response
            response = urllib.response.addinfourl(gzip_file, old_response.headers, old_response.url, old_response.code)
            response.msg = old_response.msg
        elif self._only_gzip_flag :
            raise RuntimeError("Only gzip!")
        return response

    https_request = http_request
    https_response = http_response


###
class NoRedirectHandler(urllib.request.HTTPRedirectHandler) : # pylint: disable=W0232
    def http_error_302(self, *args_tuple, **kwargs_dict) :
        return None

    http_error_301 = http_error_303 = http_error_307 = http_error_302


###
class SocksHandler(urllib.request.HTTPHandler) :
    def __init__(self, *args_tuple, **kwargs_dict) :
        self._args_tuple = args_tuple
        self._kwargs_dict = kwargs_dict
        urllib.request.HTTPHandler.__init__(self, debuglevel=kwargs_dict.pop("debuglevel", 0))

    def http_open(self, request) :
        def build(host, port = None, strict = None, timeout = socket._GLOBAL_DEFAULT_TIMEOUT) : # pylint: disable=W0212
            return SocksConnection(*self._args_tuple, host=host, port=port, strict=strict, timeout=timeout, **self._kwargs_dict)
        return self.do_open(build, request)

class SocksConnection(http.client.HTTPConnection) :
    def __init__(self, proxy_url = None, proxy_type = None, proxy_host = None, proxy_port = None,
        proxy_user = None, proxy_passwd = None, rdns_flag = True, *args_tuple, **kwargs_dict) :
        if socks is None :
            raise RuntimeError("Required module SocksiPy (the recommended is https://github.com/Anorov/PySocks)")
        http.client.HTTPConnection.__init__(self, *args_tuple, **kwargs_dict)

        if proxy_url is not None :
            parsed = urllib.parse.urlparse(proxy_url)
            scheme = parsed.scheme
            proxy_user = parsed.username
            proxy_passwd = parsed.password
            proxy_host = parsed.hostname
            proxy_port = ( parsed.port or SOCKS_PORT )
            proxy_type = SCHEME_TO_TYPE_MAP.get(( scheme or "" ).lower())
            if proxy_type is None :
                raise RuntimeError("Invalid SOCKS protocol: %s" % (scheme))

        self._proxy_args_tuple = (proxy_type, proxy_host, proxy_port, rdns_flag, proxy_user, proxy_passwd)

    def connect(self) :
        self.sock = socks.socksocket()
        self.sock.setproxy(*self._proxy_args_tuple)
        if self.timeout is not socket._GLOBAL_DEFAULT_TIMEOUT : # pylint: disable=W0212
            self.sock.settimeout(self.timeout)
        self.sock.connect((self.host, self.port))


##### PEP8 #####
tools.pep8.setupAliases()

