#:: Adeptio Dev team
#:: 2018-11-30
#:: adeptioStorade service core
#:: Alpha testing v2.2

import threading
import asyncore
import logging
import time
import sys

from config import *
from files import Files
from server import Server
from machine import Machine
from status_socket import StatusSocket

class ServerThread(threading.Thread):
    def __init__(self, host, port, listen):
        threading.Thread.__init__(self)
        self.server = Server(host, port, listen)

    def run(self):
        asyncore.loop()

    def stop(self):
    	asyncore.close_all()
    	self.server.close()
    	self.join()

class StatusThread(threading.Thread):
    def __init__(self, host, port, interval):
        threading.Thread.__init__(self)
        self.interval = interval
        self.server = StatusSocket(host, port)
        self.event = threading.Event()

    def run(self):
        while not self.event.is_set():

            self.server.send_status_info()

            self.event.wait(self.interval)

    def stop(self):
        self.event.set()
        self.server.close_socket()
        self.join()

def StorADE_close():
    logging.info("Trying to send error information")
    stat_server = StatusSocket(ADEHOST, ADEPORT, False)
    if stat_server.send_error():
        logging.info("Error information sent successful")
    else:
        logging.info("Error information sent unsuccessful")
    logging.info("StorADE closed")
    logging.shutdown()
    sys.exit()

if __name__ == "__main__":

    Files = Files()

    Files.dir_check(Files.full_path())

    Machine = Machine()

    logging.basicConfig(filename=Files.full_path(LOG_FILE), level=logging.DEBUG, format='%(asctime)s | %(levelname)s | %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

    logging.getLogger().addHandler(logging.StreamHandler())

    logging.info("StorADE started")

    try:

        __import__('OpenSSL')

    except ImportError:

        logging.critical("ImportError: No module named OpenSSL")

        StorADE_close()

    from ssl_ import SSL_

    if not Machine.get_adeptio_mn_status_check():

        logging.critical("Adeptio Masternodes working problem")

        StorADE_close()

    if not Files.dir_check(Files.full_path()):

        logging.critical("Can't create StorADE folder")

        StorADE_close()

    if not Files.dir_check(Machine.ssl_path()):

        logging.critical("Can't create SSL folder")

        StorADE_close()

    logging.info("Trying to create ssl files...")

    if not SSL_().create_ssl_files():

        logging.critical("Failure creating ssl files")

        StorADE_close()

    logging.info("SSL files created")

    logging.info("Trying to start StatusThread...")

    st = StatusThread(ADEHOST, ADEPORT, INTERVAL)

    st.start()

    if not st.is_alive():
        logging.critical("StatusThread starting error")
        st.stop()
        StorADE_close()

    logging.info("StatusThread started")

    logging.info("Trying to start ServerThread...")

    s = ServerThread(HOST, PORT, LISTEN)

    s.start()

    if not s.is_alive():
        logging.critical("ServerThread starting error")
        s.stop()
        StorADE_close()

    logging.info("ServerThread started")

    raw_input("Press any key to stop the server now...\n")

    logging.info("Trying to stop ServerThread...")

    s.stop()

    logging.info("Trying to stop StatusThread...")

    st.stop()

    StorADE_close()
