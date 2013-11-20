import unittest

from ulib import tools
import ulib.tools.unix # pylint: disable=W0611


##### Public classes #####
class TestUnix(unittest.TestCase) :
    def test_disk_free(self) :
        (full, used) = tools.unix.diskFree("/")
        self.assertTrue(full > used)

    def test_uptime(self) :
        uptime = tools.unix.uptime()
        self.assertTrue(uptime > 0)

    def test_load_average(self) :
        avg_tuple = tools.unix.loadAverage()
        for avg in avg_tuple :
            self.assertTrue(isinstance(avg, float))

