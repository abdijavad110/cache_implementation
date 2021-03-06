from json import loads as jsn_ld
from collections import namedtuple


class ReqCnf:
    read = 'R'
    write = 'W'


class FwdCnf:
    req_q_max = 10000
    res_q_max = 999999999


class CacheConf:
    """
    sizes are in Bytes.
    """
    HDDSize = 1024*1024*1024*20
    SSDSize = 1024*1024*1024*4
    RAMSize = 1024*1024*1024*1

    HDD = '/dev/sda99'
    SSD = '/dev/sdb99'
    RAM = '/dev/ram0'

    BLK_SIZE = 4096

    ram_blk = 0
    ssd_blk = 1
    hdd_blk = 2

    @staticmethod
    def get_dev(typ):
        if typ == CacheConf.ssd_blk:
            return CacheConf.SSD
        elif typ == CacheConf.ram_blk:
            return CacheConf.RAM
        elif typ == CacheConf.hdd_blk:
            return CacheConf.HDD
        else:
            raise Exception("Unknown device type!")


jsn_file = open("parser_configuration.json", 'r').read()
parser_conf = jsn_ld(jsn_file, object_hook=lambda d: namedtuple('configuration', d.keys())(*d.values()))
