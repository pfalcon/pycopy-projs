# Disk sleep (standby) monitor
# (c) 2014-2021 Paul Sokolovsky
# Based on Documentation/laptops/dslm.c from Linux kernel tree (up to v4.8).
# C version author: Bartek Kania
# Ported to Python by: Paul Sokolovsky
# Licensed under the GPL
import sys
try:
    import uos2 as os
except ImportError:
    import os
import time
import fcntl

from ioctl_linux_hdreg import *


try:
    from pyb import LED
except ImportError:
    LED = None


ACTIVE = "active"
SLEEP = "sleep"
UNKNOWN = "unknown"

led = None


def show_indicator(status):
    if led:
        if status == ACTIVE:
            led.on()
        else:
            led.off()


def check_powermode(fd):
    args = bytearray((WIN_CHECKPOWERMODE1, 0, 0, 0))
    #print(args)
    fcntl.ioctl(fd, HDIO_DRIVE_CMD, args, True)
    #print(args)
    if args[2] == 0:
        return SLEEP
    elif args[2] == 255:
        return ACTIVE
    else:
        return "unknown(%x)" % args[2]


def measure(fd):
    active_time = 0
    sleep_time = 0
    unknown_time = 0
    changes = 0
    last_state = check_powermode(fd)
    start_time = last_time = time.time()
    show_indicator(last_state)
    print("%d Starting in: %s" % (start_time, last_state))

    while True:
        time.sleep(2)
        curr_state = check_powermode(fd)
        #print(curr_state)
        if curr_state != last_state:
            show_indicator(curr_state)
            changes += 1
            curr_time = time.time()
            time_diff = curr_time - last_time

            if last_state == ACTIVE:
                active_time += time_diff
            elif last_state == SLEEP:
                sleep_time += time_diff
            else:
                unknown_time += time_diff
            print("Spent %.2fs in this mode" % time_diff)
            print("%d Switching to: %s (total: a:%.2f s:%.2f u:%.2f)" % (
                curr_time, curr_state, active_time, sleep_time, unknown_time
            ))

            last_state = curr_state
            last_time = curr_time


def __main__():
    global led

    if len(sys.argv) != 2:
        print("usage: %s /dev/sdX" % sys.argv[0])
        sys.exit(1)

    if LED:
        led = LED("power:blue")
    fd = os.open(sys.argv[1], os.O_RDONLY | os.O_NONBLOCK)
    measure(fd)


if __name__ == "__main__":
    __main__()
