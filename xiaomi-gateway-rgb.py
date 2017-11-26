# This script controls Xiaomi Mi Home Gateway RGB light.
# The gateway should have development mode enabled.
# Firmware 1.3.1_140.0141 doesn't allow to control gw LED (leads to "No device")
# Updated to 1.3.1_141.0143, then to 1.4.1_150.0143 - this works for LED, etc.
import socket
import json
import time
import ucryptolib
import binascii

MODE_CBC = 2

MULTICAST_ADDRESS = "224.0.0.50"
MULTICAST_PORT = 9898

GW_IV = b"\x17\x99\x6d\x09\x3d\x28\xdd\xb3\xba\x69\x5a\x2e\x6f\x58\x56\x2e"

# Gateway API password from app preferences, must be set by user
GW_PASSWD = b""
assert GW_PASSWD, "Set GW_PASSWD"

gw_token = None
gw_addr = None
gw_sid = None

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
addr = socket.getaddrinfo("0.0.0.0", MULTICAST_PORT)[0][-1]
sock.bind(addr)

# In case inet_pton() not implemented
#opt = socket.inet_pton(socket.AF_INET, MULTICAST_ADDRESS) + socket.inet_pton(socket.AF_INET, "0.0.0.0")
opt = bytes([224, 0, 0, 50]) + bytes([0, 0, 0, 0])
sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, opt)

print("Waiting for heardbeat message with token...")

while True:
    msg, addr = sock.recvfrom(1500)
    print(msg)
    msg = json.loads(msg.decode("utf-8"))
    if "token" in msg:
        gw_token = msg["token"]
        gw_sid = msg["sid"]
        data = json.loads(msg["data"])
        gw_addr = data["ip"]
        break

print("Received token:", gw_token)

def make_key():
    cipher = ucryptolib.aes(GW_PASSWD, MODE_CBC, GW_IV)
    key = binascii.hexlify(cipher.encrypt(gw_token)).decode()
    return key

def run():
    sock.connect((gw_addr, MULTICAST_PORT))
    key = make_key()

    rgb = 0x0000ff
    for i in range(3):
        # Brightness, then RGB
        data = {"key": key, "rgb": 0x07000000 | rgb}
        data = json.dumps(data)
        cmd = {"cmd": "write", "model": "gateway", "sid": gw_sid, "data": data}
        cmd = json.dumps(cmd)
        print("cmd:", cmd.encode())

        sock.send(cmd)

        data, addr = sock.recvfrom(1500)
        print("resp:", data)

        rgb <<= 8
        time.sleep(1)


run()
