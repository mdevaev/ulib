# -*- coding: utf-8 -*-


import httplib


##### Exceptions #####
class BadRequest(Exception) :
    def __init__(self, code, text) :
        super(BadRequest, self).__init__()
        self.__code = code
        self.__text = text

    def text(self) :
        return self.__text

    def __str__(self) :
        return "%d %s" % (self.__code, httplib.responses[self.__code])

