import re
import socket

from ulib import validatorlib


##### Public methods #####
def validIpOrHost(arg) :
    name = "IPv4/IPv6 address or RFC-1123 hostname"
    arg = validatorlib.notEmptyStrip(arg, name)
    return validatorlib.checkChain(arg, (
            validIpAddress,
            lambda arg : (validRfcHost(arg), None),
        ), name)

def validIpAddress(arg) :
    name = "IPv4/IPv6 address"
    arg = validatorlib.notEmptyStrip(arg, name)
    return validatorlib.checkChain(arg, (
            lambda arg, : ((arg, socket.inet_pton(socket.AF_INET, arg))[0], socket.AF_INET ),
            lambda arg, : ((arg, socket.inet_pton(socket.AF_INET6, arg))[0], socket.AF_INET6 ),
        ), name)

def validRfcHost(arg) :
    # XXX: See http://stackoverflow.com/questions/106179/regular-expression-to-match-hostname-or-ip-address
    return validatorlib.checkRegexp(arg,
        r"^(([a-zA-Z0-9]|[a-zA-Z0-9][a-zA-Z0-9\-]*[a-zA-Z0-9])\.)*([A-Za-z0-9]|[A-Za-z0-9][A-Za-z0-9\-]*[A-Za-z0-9])$",
        "RFC-1123 hostname",
    )

def validPort(arg) :
    name = "TCP/UDP portnumber"
    arg = validatorlib.notEmptyStrip(arg, name)
    try :
        if not (0 <= int(arg) < 65536) :
            raise Exception
        return int(arg)
    except Exception :
        validatorlib.raiseError(arg, name)

def validBsdAddress(arg) :
    name = "BSD address"
    arg = validatorlib.notEmptyStrip(arg, name)
    address_match = re.match(r"^(.+)\.(\d+)$", arg)
    if address_match is None :
        validatorlib.raiseError(arg, name)
    return (arg, (validRfcHost(address_match.group(1)), validPort(address_match.group(2))))

