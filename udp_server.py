import socket
import json
import errno
import sys
import admin
from time import sleep

# TODO: Request UAC elevation for windows platforms
# TODO: Insure cross-platform compatibility in general

class udpServer:

    def __init__(self, udp_ip=None):
        self.ip = udp_ip
        self.port = 11600
        self.sock = socket.socket(socket.AF_INET,
                             socket.SOCK_DGRAM)
        self.broadcast = "255.255.255.255"
        if self.ip is None:
            self.find_station()

    def find_station(self):
        print('No IP set, searching for Q station...')
        ping = json.dumps({'cmd': 'ping'})
        self.sock.bind(('127.0.0.1', self.port))
        self.sock.sendto(ping, ('255.255.255.255', self.port))
        while True:
            try:
                data, addr = self.sock.recv(1024)
            except socket.error, e:
                err = e.args[0]
                if err == errno.EAGAIN or err == errno.EWOULDBLOCK:
                    sleep(1)
                    print('No data available')
                    continue
                else:
                    print e
                    sys.exit(1)
            else:
                if 'belleds' in data:
                    print('Q station found:' + data)
                    data_list = data.split(',')
                    self.ip = data_list[1]
                    if self.port != data_list[2]:
                        self.port = data_list[2]
                    break
                else:
                    print('No Q station found')
                    break



