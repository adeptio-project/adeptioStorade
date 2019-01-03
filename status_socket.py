import socket
import ssl

from config import *
from auth import Auth
from machine import Machine
from request_formatting import RequestFormatting

class StatusSocket(Auth, RequestFormatting, Machine):
    def __init__(self, host, port, ssl = True):
        self.host = host
        self.port = port
        self.ssl = ssl

    def create_socket(self):

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        #self.create_socket(socket.AF_INET6, socket.SOCK_STREAM) #IPv6

        #serv.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)

    def connect(self):

        try:

            self.socket.connect( (self.host, self.port) )
            
        except:

            return False

        if self.ssl:

            self.socket = ssl.wrap_socket(self.socket, certfile=self.ssl_path(STATUS_CERTFILE), keyfile=self.ssl_path(STATUS_KEYFILE))

        return True

    def close_socket(self):

        if hasattr(self, 'socket'):

            self.socket.close()

    def send(self, data):

        if not self.ssl:

            data = self.str_encode(data, 'StorADE Beta')

        return self.socket.send(data)

    def read(self):
        recv = self.socket.recv(BUFSIZE)

        cms, auth, size, data = self.parse_request(recv)

        if data.get('success') and data.get('auth'):

            self.save_auth(data['auth'])

    def write(self):
        data = self.make_request('STAT', self.full_info())

        self.send(data)

    def read_log(self):
        
        return self.socket.recv(BUFSIZE)

    def write_log(self):
        message = ";;;\n".join(self.get_last_log(20))

        data = self.make_request('STAT', message)

        self.send(data)

    def send_status_info(self):

        self.create_socket()
        if self.connect():
            self.write()
            self.read()
            self.close_socket()

    def send_error(self):

        r = False
        self.create_socket()
        if self.connect():
            self.write_log()
            r = self.read_log()
            self.close_socket()

        return r