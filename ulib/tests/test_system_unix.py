import unittest
import os

from .. import tools
import ulib.tools.pep8 # pylint: disable=W0611

from .. import system
import ulib.system.unix


##### Public classes #####
@unittest.skipIf(os.name != "posix", "posix only")
class TestUnix(unittest.TestCase) :
    def test_disk_free(self) :
        (full, used) = system.unix.diskFree("/")
        self.assertTrue(full > used)

    def test_uptime(self) :
        uptime = system.unix.uptime()
        self.assertTrue(uptime > 0)

    def test_load_average(self) :
        avg_tuple = system.unix.loadAverage()
        for avg in avg_tuple :
            self.assertTrue(isinstance(avg, float))


##### PEP8 #####
tools.pep8.setupAliases()

