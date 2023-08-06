from mipea import gpio
import time

out = gpio.GPIO(26, True)
inp = gpio.GPIO(16, pull=gpio.PULL_UP)

while inp.tst():
    out.set()
    time.sleep(1)
    out.clr()
    time.sleep(1)
