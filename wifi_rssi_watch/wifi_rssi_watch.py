import network
import time

sta = network.WLAN(network.STA_IF)
start = time.time()


def get_rssi(ssid):
    res = sta.scan()
    #print(res)
    e = [x for x in res if x[0] == ssid]
    if not e:
        return None
    return e[0][3]

def elapsed():
    t = int(time.time() - start)
    return "%02d:%02d" % (t // 60, t % 60)


def main(ssid):
    rssi_min = 0
    rssi_max = -10000
    scan_failed = 0
    scan_miss = 0

    while True:
        try:
            rssi = get_rssi(ssid)
            if rssi is None:
                scan_miss += 1
        except OSError as e:
            print(repr(e))
            scan_failed += 1
            rssi = None
            time.sleep(3)
        if rssi is not None:
            rssi_min = min(rssi_min, rssi)
            rssi_max = max(rssi_max, rssi)
        print("%s min: %s cur: %s max: %s missed: %d failed: %d" % \
            (elapsed(), rssi_min, rssi, rssi_max, scan_miss, scan_failed))
        time.sleep(1)

# To use this script:
#import wifi_rssi_watch
#wifi_rssi_watch.main(b"my-access-point")
