from network import WLAN
import time
import socket

wlan = WLAN()
wlan.init()
networks = wlan.scan()

for net in enumerate(networks):
    if net[1][0] == "eatme":
        server = net[1]

wlan.connect(ssid=server[0],auth=(WLAN.WPA2,'98f7V4]6'))
while not wlan.isconnected():
    time.sleep_ms(50)

mySocket = socket.socket( socket.AF_INET, socket.SOCK_DGRAM )
mySocket.connect(('192.168.137.1',5000))

while True:
    mySocket.send('HI')
    time.sleep(3)



# OLD SERVER

mySocket = socket( AF_INET, SOCK_DGRAM )
mySocket.bind( ('0.0.0.0', 5000) )

mySocket.listen()
sock, addr = mySocket.accept()

print(addr)

while True:
    time.sleep(0.1)
    data = sock.recv(SIZE)
    print(data)