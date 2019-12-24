"""
run this file to see a sample of how to work with forwarder module.
"""
from time import sleep

from forwarder import Forwarder, Request


if __name__ == '__main__':
    ff = Forwarder()
    ff.issue(Request('/dev/sdc2', 0, 0, length=100))
    ff.issue(Request('/dev/sdc2', 0, 90, length=100))
    ff.issue(Request('/dev/sdc2', 1, 100, data=b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'))
    ff.issue(Request('/dev/sdc2', 1, 0, data=b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'))
    ff.issue(Request('/dev/sdc2', 0, 0, length=100))
    ff.issue(Request('/dev/sdc2', 0, 90, length=100))
    sleep(3)
    print(ff.res_Q.pop().data)
    print(ff.res_Q.pop().data)
    print(ff.res_Q.pop().latency)
    print(ff.res_Q.pop().latency)
    print(ff.res_Q.pop().data)
    print(ff.res_Q.pop().data)
