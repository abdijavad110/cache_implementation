import threading
from time import time

from conf import FwdCnf, ReqCnf


class Request:
    def __init__(self, dst, typ, addr, length=512, data=None):

        """
        Request class holds each request properties
        :param dst: target device in form of /dev/TARGET_DEVICE
        :param typ: request type (read or write) from ReqCnf types
        :param addr: request starting address. should be multiply of 512
        :param length: request length. ignored in writes. pay attention to data length
        :param data: data req want to write in the form of '\\xOO\\xOO ...' where OO is the bytes
        """

        self.dest = dst
        self.type = typ
        self.addr = addr
        self.len = length
        self.data = data
        self.latency = -1

    def load_data(self, data):
        self.data = data


class Queue:
    def __init__(self, max_size=None, zero_out=False):
        self.queue = []
        self.lock = threading.Lock()
        if zero_out:
            self.semaphore = threading.BoundedSemaphore(max_size)
            for _ in range(max_size):
                self.semaphore.acquire()
        else:
            self.semaphore = threading.Semaphore(0)

    def append(self, data):
        self.lock.acquire()
        self.queue.append(data)
        self.lock.release()
        print("releasing the semaphore")
        self.semaphore.release()

    def pop(self, k=0):
        print("acquiring the semaphore")
        self.semaphore.acquire()
        self.lock.acquire()
        res = self.queue.pop(k)
        self.lock.release()
        return res

    def len(self):
        return self.queue.__len__()


class Forwarder:
    def __init__(self):
        """
        req_Q accepts up to FwdCnf.req_q_max requests
        pay attention to free res_Q, if len exceed FwdCnf.res_q_max then deadlock will happen
        """
        self.req_Q = Queue(FwdCnf.req_q_max, zero_out=True)
        self.res_Q = Queue(FwdCnf.res_q_max)

        self.fwd_trd = threading.Thread(target=self.forward_service, daemon=True)
        self.fwd_trd.start()

    def issue(self, req):
        self.req_Q.append(req)

    def forward_service(self):
        while True:
            req = self.req_Q.pop()
            start = time()

            if req.type == ReqCnf.read:
                dd = open(req.dest, 'rb')
                dd.seek(req.addr)
                res = dd.read(req.len)
                req.load_data(res)
            else:
                dd = open(req.dest, 'wb')
                dd.seek(req.addr)
                dd.write(req.data)
            dd.close()

            req.latency = time() - start
            self.res_Q.append(req)
