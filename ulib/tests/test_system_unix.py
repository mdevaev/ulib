import unittest
import os

from ulib import system
import ulib.system.unix # pylint: disable=W0611


##### Public classes #####
class TestUnix(unittest.TestCase) :
    @unittest.skipIf(os.name != "posix", "posix only")
    def test_disk_free(self) :
        (full, used) = system.unix.diskFree("/")
        self.assertTrue(full > used)

    @unittest.skipIf(os.name != "posix", "posix only")
    def test_uptime(self) :
        uptime = system.unix.uptime()
        self.assertTrue(uptime > 0)

    @unittest.skipIf(os.name != "posix", "posix only")
    def test_load_average(self) :
        avg_tuple = system.unix.loadAverage()
        for avg in avg_tuple :
            self.assertTrue(isinstance(avg, float))

