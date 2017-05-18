import sys
import time
import socket
import esp
import network

#sta = network.WLAN(network.STA_IF)
#sta.active(1); sta.connect()


def dl(url, debug=False):
    import uhashlib
    import ubinascii

    proto, dummy, host, path = url.split("/", 3)
    ai = socket.getaddrinfo(host, 80)
    addr = ai[0][4]
    s = socket.socket()
    s.settimeout(10)
    try:
        s.connect(addr)
        s.write(b"GET /%s HTTP/1.0\r\nHost: %s\r\n\r\n" % (path, host))
        size = 0
        hash = uhashlib.sha1()
        t = time.ticks_ms()
        buf = s.read(2000)
        assert buf, buf
        if debug:
            print("initial response:", buf)
        header, buf = buf.split(b"\r\n\r\n", 1)
        #print(header)
        #print(buf)
        hash.update(buf)
        size += len(buf)
        while 1:
            buf = s.read(1024)
            if buf == b"": break
            hash.update(buf)
            size += len(buf)
            sys.stdout.write("%dK\r" % (size >> 10))
#            sta.active(False)
        delta = time.ticks_diff(time.ticks_ms(), t)
        #print()
        print("Size :", size)
        print("Speed: %s bytes/s" % (size / delta * 1000))
        print("Elapsed: %s" % (delta / 1000))
        sha = str(ubinascii.hexlify(hash.digest()), "ascii")
        print("SHA1 :", sha)
        return size, sha
    finally:
        s.close()


# http://archive.ubuntu.com/ubuntu/dists/xenial/main/installer-amd64/current/images/
# http://archive.ubuntu.com/ubuntu/dists/xenial/main/installer-amd64/current/images/hd-media/

FILES = [
    # 6.7M
    ("http://archive.ubuntu.com/ubuntu/dists/xenial/main/installer-amd64/current/images/hd-media/vmlinuz",
     "337c37d7ec00348414224baa6bdb2d43f2a34ef5676bafcdcad916f148b5b317"),
    # 23M
#    ("http://archive.ubuntu.com/ubuntu/dists/xenial/main/installer-amd64/current/images/hd-media/boot.img.gz",
#     "30a6ebda5b3f7e2c3131ef99272fea47c0ec153c7a99f358ce1ce653b1eb23b2"),
#    ("http://archive.ubuntu.com/ubuntu/dists/xenial/main/installer-amd64/current/images/udeb.list",
#     "eb26cc410b9d60eb0ab927bd972ae09fe47431de"),
]

def main():
    total = 0
    fails = 0
    while 1:
        for url, exp_sha in FILES:
            try:
                size, sha = dl(url)
            except OSError as e:
                sys.print_exception(e)
                print("ESP bufs: tx:%d rx:%d" % (esp.esf_free_bufs(0), esp.esf_free_bufs(4)))
                fails += 1
                time.sleep(2)
                continue
            total += size
            if sha != exp_sha:
                print("INVALID SHA1")
            print("Total downloaded so far: %dM" % (total >> 20))

main()
