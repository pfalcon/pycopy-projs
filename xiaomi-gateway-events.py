# This script subscribes to Xiaomi Mi Home Gateway notifications and
# dumps them. The gateway should have development mode enabled.
import socket
import json
import time

MULTICAST_ADDRESS = "224.0.0.50"
MULTICAST_PORT = 9898

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
addr = socket.getaddrinfo("0.0.0.0", MULTICAST_PORT)[0][-1]
sock.bind(addr)

# In case inet_pton() not implemented
#opt = socket.inet_pton(socket.AF_INET, MULTICAST_ADDRESS) + socket.inet_pton(socket.AF_INET, "0.0.0.0")
opt = bytes([224, 0, 0, 50]) + bytes([0, 0, 0, 0])
sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, opt)

while True:
    data, addr = sock.recvfrom(1500)
    data = json.loads(data.decode("utf-8"))
    print("%s: %s: message: %s" % (time.time(), addr, data))
