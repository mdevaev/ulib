# -*- coding: utf-8 -*-


import os


##### Public methods #####
def diskFree(path) :
    statvfs = os.statvfs(path)
    assert not statvfs is None
    full = statvfs.f_blocks * statvfs.f_bsize
    free = statvfs.f_bavail * statvfs.f_bsize
    return (full, full - free)

def uptime() :
    with open("/proc/uptime") as uptime_file :
        return float(uptime_file.readline().split()[0])

def loadAverage() :
    with open("/proc/loadavg") as loadavg_file :
        return tuple(map(float, loadavg_file.readline().split()[:3]))

