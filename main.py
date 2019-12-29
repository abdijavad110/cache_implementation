import threading
from tqdm import tqdm

from parser import Parser
from forwarder import Forwarder


if __name__ == '__main__':
    parsers = [
        Parser('trace/NEW_2016031907-LUN1.csv'),
        Parser('trace/NEW_2016031907-LUN4.csv')
    ]
    forwarder = Forwarder(concurrency=10)

    llt = 0
    for parser in parsers:
        llt += parser.cnt
        threading.Thread(
            target=parser.start_sending_requests,
            args=(forwarder.issue,),
            daemon=True
        ).start()

    lats = []
    cnt = 0
    with tqdm(total=llt) as pbar:
        try:
            while True:
                cnt += 1
                if cnt == 500:
                    pbar.update(cnt)
                    cnt = 0
                res = forwarder.res_Q.pop()
                lats.append(res.latency*1000)

        except KeyboardInterrupt:
            pbar.update(cnt)
            print("\n\naverage latency= %.3fms" % (sum(lats)/len(lats)))
            print("maximum latency= %.3fms" % max(lats))
            print("minimum latency= %.3fms\n" % min(lats))
