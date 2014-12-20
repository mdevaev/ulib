import sys
import traceback

from .. import tools
import ulib.tools.pep8 # pylint: disable=W0611


##### Public methods #####
def oneLine(text, short_flag = True, output = sys.stdout, static_list = [""]) : # pylint: disable=W0102
    old_text = static_list[0]
    if short_flag :
        static_list[0] = text
        text = " "*len(old_text) + "\r" + text + "\r"
    else :
        if len(static_list[0]) != 0 :
            text = " "*len(old_text) + "\r" + text + "\n"
        else :
            text += "\n"
        static_list[0] = ""
    output.write(text)
    output.flush()

def newLine(text, output = sys.stdout) :
    oneLine(text, False, output)

def printTraceback(prefix = "", output = sys.stdout) :
    for row in traceback.format_exc().strip().split("\n") :
        print(prefix + row, file=output)


##### PEP8 #####
tools.pep8.setupAliases()

