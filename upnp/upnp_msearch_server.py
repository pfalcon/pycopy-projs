import socket
from binascii import hexlify
try:
    from socket import sockaddr
except:
    sockaddr = lambda x: x


UPNP_MCAST_IP = "239.255.255.250"
UPNP_PORT = 1900
BIND_IP = "0.0.0.0"
# The obvious solution is to send UPNP responses using the same
# socket used to receive multicast requests (and thus bound to
# port 1900), but there're some braindead UPNP implementation
# which don't like that, so conservatively open 2nd socket just
# for responses.
REUSE_SOCKET = 0

UPNP_RESPONSE = b"""HTTP/1.1 200 OK\r
CACHE-CONTROL: max-age=100\r
EXT:\r
Location: http://localhost:8080/description.xml\r
Server: dummy/1.0, UPnP/1.0\r
ST: upnp:rootdevice\r
USN: uuid:12345678-9abc-1111-2222-foo::upnp:rootdevice\r
\r
"""


serv_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

addr = socket.getaddrinfo(BIND_IP, UPNP_PORT, socket.AF_INET, socket.SOCK_DGRAM)[0][4]
serv_sock.bind(addr)
serv_sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, socket.inet_aton(UPNP_MCAST_IP) + socket.inet_aton(BIND_IP));
if REUSE_SOCKET:
    resp_sock = serv_sock
else:
    resp_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

while True:
    data, addr = serv_sock.recvfrom(1024)
    if data.startswith(b"M-SEARCH"):
        print("From: ", sockaddr(addr))
        print(data)
        resp_sock.sendto(UPNP_RESPONSE, addr)
