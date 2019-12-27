from conf import CacheConf


class BaseMapping:
    def __init__(self, total):
        self.total = total // CacheConf.BLK_SIZE
        self.map_table = {}
        self.free = list(range(0, total - CacheConf.BLK_SIZE + 1, CacheConf.BLK_SIZE))

    def map(self, la):
        try:
            return self.map_table[la]
        except KeyError:
            free = self.free.pop()
            self.map_table[la] = free
            return free

    def invalidate(self, la):
        try:
            self.free.append(self.map_table.pop(la))
        except KeyError:
            pass


class Tables:
    SSD = BaseMapping(CacheConf.SSDSize)
    RAM = BaseMapping(CacheConf.RAMSize)
