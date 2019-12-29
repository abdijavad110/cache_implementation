from conf import CacheConf
from mapping import Tables
from forwarder import Forwarder, Request


class Proxy:
    forwarder = Forwarder()

    def __init__(self):
        raise Exception('Proxy is a static class, so can not be instantiated.')

    @staticmethod
    def invalidate(blk):
        if blk.typ == CacheConf.ram_blk:
            Tables.RAM.invalidate(blk.addr)
        elif blk.typ == CacheConf.ssd_blk:
            Tables.SSD.invalidate(blk.addr)

    @staticmethod
    def promote(blk, dst):
        pass

    @staticmethod
    def write(blk):
        Proxy.forwarder.issue(Request(CacheConf.get_dev(blk.typ), blk.typ, blk.addr, data=b'\x00' * blk.len))

    @staticmethod
    def read(blk):
        Proxy.forwarder.issue(Request(CacheConf.get_dev(blk.typ), blk.typ, blk.addr, length=blk.len))
