# -*- coding: utf-8 -*-


import httplib


##### Exceptions #####
class ServerError(Exception) :
    def __init__(self, code, text) :
        super(ServerError, self).__init__()
        self.__code = code
        self.__text = text
        self.__message = httplib.responses[code]

    def code(self) :
        return self.__code

    def message(self) :
        return self.__message

    def info(self) :
        return "%d %s" % (self.__code, self.__message)

    def text(self) :
        return self.__text

    def __str__(self) :
        return "%d %s [%s]" % (self.__code, self.__message, self.__text)

