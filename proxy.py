from conf import CacheConf
from mapping import Tables


class Proxy:
    def __init__(self):
        pass

    def invalidate(self, blk):
        pass

    def promote(self, blk, dst):
        pass

    def write(self, blk):
        pass

    def read(self, blk):
        pass
