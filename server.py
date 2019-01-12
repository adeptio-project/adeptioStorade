import asyncore
import logging
import socket
import ssl

from asyncore import compact_traceback

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

    def handle_accept(self):
        pair = self.accept()

        if pair is not None: #Server received and accept new client!

            sock, addr = pair

            ip, port = addr

            client_name = str(ip) + ":" + str(port)

            if not self.allow_client(ip):

                sock.close()

                logging.info('Incoming connection from %s was rejected', client_name)

                return

            logging.info('Incoming connection from %s', client_name)

            sock.settimeout(CLIENT_TIMEOUT) #If client conncect without ssl must not stuck here
            
            sock = ssl.wrap_socket(sock, server_side=True, certfile=self.ssl_path(STORADE_CERTFILE), keyfile=self.ssl_path(STORADE_KEYFILE)) #ssl_version=PROTOCOL_TLS, ca_certs=None
            
            Client(sock, addr) #Send accepted client to Client function!

    def handle_error(self):
        nil, t, v, tbinfo = compact_traceback()

        # sometimes a user repr method will crash.
        try:
            self_repr = repr(self)
        except:
            self_repr = '<__repr__(self) failed for object at %0x>' % id(self)

        try:
            v = str(v)
        except:
            v = ''

        if not 'The handshake operation timed out' in v and not 'http request' in v:

            logging.critical(
                'uncaptured python exception, closing channel %s (%s:%s %s)',
                    self_repr,
                    t,
                    v,
                    tbinfo
                )

            self.handle_close()

    def handle_close(self):

        logging.info('Server is closing on %i port', self.port)

        self.close()

    def allow_client(self, ip):

        if self.local_ip(ip):

            return True

        try:

            if ip in self.get_clients_list():

                return True

        except:
            return False