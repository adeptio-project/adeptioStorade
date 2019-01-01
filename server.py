import asyncore
import logging
import socket
import ssl

from config import *
from client import Client
from machine import Machine

class Server(asyncore.dispatcher, Machine):

    def __init__(self, host, port, listen):
        asyncore.dispatcher.__init__(self)
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        #self.create_socket(socket.AF_INET6, socket.SOCK_STREAM) #IPv6
        #self.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
        self.set_reuse_addr() # try to re-use a server port if possible
        self.bind((host, port))
        self.listen(listen)
        self.port = port
        logging.info("Server is ready and listening on %i port", self.port)

    def getclientname(self, addr):
        ip, port = addr

        return ip + ":" + str(port)

    def handle_accept(self):
        pair = self.accept()

        if pair is not None: #Server received and accept new client!

            sock, addr = pair

            if not self.allow_client(addr):

                sock.close()

                logging.info('Incoming connection from %s was rejected', self.getclientname(addr))

                return

            logging.info('Incoming connection from %s', self.getclientname(addr))

            #If client conncect without ssl must not stuck here

            sock = ssl.wrap_socket(sock, server_side=True, certfile=self.ssl_path(STORADE_CERTFILE), keyfile=self.ssl_path(STORADE_KEYFILE)) #ssl_version=PROTOCOL_TLS, ca_certs=None

            Client(sock) #Send accepted client to Client function!

    def handle_close(self):

        logging.info('Server is closing on %i port', self.port)

        self.close()

    def allow_client(self, addr):
        ip, port = addr
        if self.local_ip(ip):
            return True
        clients = self.get_clients_list()
        if clients:
            if ip in clients:
                return True
        return False
        