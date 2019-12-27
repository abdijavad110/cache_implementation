class ReqCnf:
    read = 0
    write = 1


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

    BLK_SIZE = 4096
