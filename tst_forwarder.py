import unittest
from time import sleep
from random import randint

from forwarder import Forwarder, Request


class MyTestCase(unittest.TestCase):
    def test_something(self):
        try:
            ff = Forwarder(concurrency=10)

            for _ in range(2000):
                ff.issue(
                    Request('/dev/ram0', randint(0, 1), randint(0, 1024 * 1024 * 500), length=512, data=b'\xcd' * 512))
            sleep(0.5)
            lat = 0
            for i in range(2000):
                res = ff.res_Q.pop()
                lat = (lat * i + res.latency) / (i + 1)
                # print(res.addr, res.type, res.latency * 1000)
            print("\nmean latency = %f" % (lat * 1000))
            self.assertTrue('mean latency = %f' % (lat * 1000))
        except Exception as e:
            self.assertFalse(e.__traceback__)


if __name__ == '__main__':
    unittest.main()
