import logging
from asyncore import dispatcher

from config import *
from do import Do

class Client(dispatcher):

    def __init__(self, sock, addr, map=None):
        dispatcher.__init__(self, sock, map)

        self.get_data = self.send_data = 0
        self.client_ip, self.client_port = addr
        self.client_name = str(self.client_ip) + ":" + str(self.client_port)

        self.do = Do(addr)

    def handle_close(self):

        if DEBUG:
            logging.debug('Disconnected from %s client from which got %i bytes and send %i bytes', self.client_name, self.get_data, self.send_data)
        else:
            logging.info('Disconnected from %s client', self.client_name)

        self.close()

    def handle_read(self):

        data = self.recv(BUFSIZE)

        if data:

            l = len(data)

            self.get_data += l

            if DEBUG:
               logging.debug('Got data from %s client (%i): %s', self.client_name, l, data)

            self.do.request(data)

    def handle_write(self):

        data = self.do.out_buffer
        self.do.out_buffer = self.do.out_buffer.replace(data, '')

        if data:

            l = len(data)

            self.send_data += l

            if DEBUG:
                logging.debug('Sending data to %s client (%i): %s', self.client_name, l, data)

            self.send(data)

    def writable(self):
        return (not self.connected) or len(self.do.out_buffer)

    def send(self, data):
        num_sent = 0
        num_sent = dispatcher.send(self, data[:512])
        data = data[num_sent:]

        self.do.out_buffer = data + self.do.out_buffer

        #Check if reading is finished

        if self.do.close_when_done and self.do.out_buffer == '':

            self.handle_close()