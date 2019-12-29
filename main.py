import threading

from parser import Parser
from forwarder import Forwarder


if __name__ == '__main__':
    parser1 = Parser('trace/NEW_2016031907-LUN1.csv')
    parser2 = Parser('trace/NEW_2016031907-LUN4.csv')
    forwarder = Forwarder(concurrency=10)

    for parser in [parser1, parser2]:
        threading.Thread(
            target=parser.start_sending_requests,
            args=(forwarder.issue,),
            daemon=True
        ).start()

    lats = []
    try:
        while True:
            res = forwarder.res_Q.pop()
            lats.append(res.latency*1000)
            # print("%s in %d ==> %fms" % (res.type, res.addr, res.latency*1000))
    except KeyboardInterrupt:
        print("\n\naverage latency= %.3fms" % (sum(lats)/len(lats)))
        print("maximum latency= %.3fms" % max(lats))
        print("minimum latency= %.3fms\n" % min(lats))
