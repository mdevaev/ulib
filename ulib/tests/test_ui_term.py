import sys
import os
import io
import unittest

from .. import tools
import ulib.tools.pep8 # pylint: disable=W0611

from .. import ui
import ulib.ui.term


##### Public classes #####
class TestTerm(unittest.TestCase) :
    def test_colored(self) :
        result = ( "\x1b[31;47mTest\x1b[0m" if os.name == "posix" else "Test" )
        self.assertEqual(ui.term.colored((31, 47), "Test", True), result)

    def test_colored_raw(self) :
        result = ( ("\x1b[31;47m", "Test", "\x1b[0m") if os.name == "posix" else ("", "Test", "") )
        self.assertEqual(ui.term.colored((31, 47), "Test", True, True), result)

    def test_colored_stringio(self) :
        self.assertEqual(ui.term.colored((31, 47), "Test", output=io.StringIO()), "Test")

    def test_colored_stringio_raw(self) :
        self.assertEqual(ui.term.colored((31, 47), "Test", raw_flag=True, output=io.StringIO()), ("", "Test", ""))

    ###

    @unittest.skipIf(not sys.stdout.isatty(), "stdout is not terminal")
    def test_terminal_size(self) :
        (columns, lines) = ui.term.terminalSize(2, 1, -2, -1)
        self.assertGreater(columns, 2)
        self.assertGreater(lines, 1)

    @unittest.skipIf(not sys.stdout.isatty(), "stdout is not terminal")
    def test_terminal_size_min(self) :
        (columns, lines) = ui.term.terminalSize(2000, 1000, -2, -1)
        self.assertEqual(columns, 2000)
        self.assertEqual(lines, 1000)


##### PEP8 #####
tools.pep8.setupAliases()

