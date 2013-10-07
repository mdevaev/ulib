# -*- coding: utf-8 -*-


##### Public methods #####
def utf8(line) :
    return ( line.encode("utf-8") if isinstance(line, unicode) else str(line) )

def fromUtf8(line) :
    return ( line.decode("utf-8") if isinstance(line, str) else unicode(line) )

def replaceStrInvalids(line) :
    return ( line.decode("utf-8", "replace").encode("utf-8") if isinstance(line, str) else line )

