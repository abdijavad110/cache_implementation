from conf import parser_conf as conf
from time import sleep, time
from tqdm import tqdm

from forwarder import Request


class Parser:
    def __init__(self, file_path=conf.traceFilePath):
        with tqdm(total=4, desc='parsing trace file') as tq:
            trace = open(file_path).read().split("\n")
            tq.update()
            trace = list(map(lambda q: q.split(conf.traceDil), trace))
            tq.update()
            trace = [e for e in trace if len(e) == conf.indicesCnt]
            tq.update()

            self.requests = list(map(
                lambda q: [(float(q[conf.timeInd])-float(trace[0][conf.timeInd]))*conf.delayFactor,
                           q[conf.RWInd], int(q[conf.addrInd]), int(q[conf.sizeInd])],
                trace))
            tq.update()
        self.cnt = len(self.requests)
        tq.close()
        self.currentRequest = 0

    def start_sending_requests(self, dest):
        start = time()
        for req in self.requests:
            while time() - start < req[0]:
                sleep(2/1000000)
            if req[1] == 'W':
                dest(Request(conf.storageDevice, req[1], req[2] % conf.storageCapacity, data=b'\x12' * req[3]))
            else:
                dest(Request(conf.storageDevice, req[1], req[2] % conf.storageCapacity, length=req[3]))
            self.currentRequest += 1
