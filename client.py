import asyncore
import logging

from config import *
from do import Do

class Client(asyncore.dispatcher_with_send):

    do = None
    temp = ''
    get_data = 0
    send_data = 0

    def getclientname(self):

        ip, port = self.getpeername()

        return ip + ":" + str(port)

    def handle_close(self):

        if DEBUG:
            logging.info('Disconnected from %s client from which got %i bytes and send %i bytes', self.getclientname(), self.get_data, self.send_data)

        self.close()

    def handle_read(self):
        self.close_when_done = 0

        data = self.recv(BUFSIZE)

        if data:

            if DEBUG:
               logging.debug('From %s got message: %s', self.getclientname(), data)

            self.get_data += len(data)

            if self.do == None:

                self.do = Do(self.getclientname(), data)

            else:

                self.do.request(data)

            self.temp = self.do.out_buffer

            if DEBUG:
        	   logging.info('Get %i bytes data from %s client', len(data), self.getclientname())

    def writable(self):
        return (not self.connected) or len(self.temp)

    def handle_write(self):

        if self.do != None:

            if DEBUG:
                logging.info('Sending data to %s client', self.getclientname())

            self.send_data += len(self.do.out_buffer)
            self.send(self.do.out_buffer)

            self.do.out_buffer = self.out_buffer
            self.temp = self.do.out_buffer

            if self.do.close_when_done and self.out_buffer == '':

                self.handle_close()
                
                self.close_when_done = 0