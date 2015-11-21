#https://embeddedinn.wordpress.com/tutorials/upnp-device-architecture/
import socket
from binascii import hexlify
try:
    from socket import sockaddr
except:
    sockaddr = lambda x: x

UPNP_MCAST_IP = "239.255.255.250"
UPNP_PORT = 1900

M_SEARCH = b"""\
M-SEARCH * HTTP/1.1\r
Host: 239.255.255.250:1900\r
MAN: ssdp:discover\r
ST: upnp:rootdevice\r
MX: 2\r
\r
"""
#ST: ssdp:all\r

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

addrs = socket.getaddrinfo(UPNP_MCAST_IP, UPNP_PORT, socket.AF_INET, socket.SOCK_DGRAM)
#for a in addrs:
#    print(a)

s.sendto(M_SEARCH, addrs[0][4])

while True:
    data, addr = s.recvfrom(1024)
    print("Received from:", sockaddr(addr))
    #print(hexlify(addr))
    print(str(data, "utf-8"))
