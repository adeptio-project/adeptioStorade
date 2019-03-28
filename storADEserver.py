#:: Adeptio Dev team
#:: 2018-12-18
#:: adeptioStorade service core
#:: Alpha testing v1.0

import threading
import asyncore
import logging
import time
import sys

from config import *
from helper import *
from files import Files
from server import Server
from machine import Machine
from status_socket import StatusSocket

class ServerThread(threading.Thread):
    def __init__(self, host, port, listen, prot):
        threading.Thread.__init__(self)
        self.server = Server(host, port, listen, prot)

    def run(self):
        asyncore.loop(LOOP_TIMEOUT)

    def stop(self):
    	asyncore.close_all()
    	self.server.handle_close()
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

    Machine = Machine()

    check = {
             "Can't create StorADE folder": Files.dir_check(Files.full_path()), 

             "Can't create SSL folder": Files.dir_check(Machine.ssl_path()), 

             "ImportError: No module named OpenSSL": import_check('OpenSSL'), 

             "Can't create clients list file": Machine.create_clients_list() > 1,

             "Can't find working masternode": Machine.check_adeptio_mn_status(),

             "Can't get masternodes list": Machine.check_adeptio_mn_list(),

             "Can't get masternode ip": Machine.check_adeptio_mn_ip(),

             "Can't find " + ADEPTIO_PATH + " file": Files._is_file(ADEPTIO_PATH)
            }



    logging.basicConfig(filename=Files.full_path(LOG_FILE), level=logging.DEBUG, format='%(asctime)s | %(levelname)s | %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

    logging.getLogger().addHandler(logging.StreamHandler())



    logging.info("StorADE started")



    for error, exist in check.items():

        if not exist:

            logging.critical(error)

    if False in check.values():

        StorADE_close()



    #Check if port is free



    logging.info("Trying to create ssl files...")

    from ssl_ import SSL_

    if not SSL_().create_ssl_files():

        logging.critical("Failure creating ssl files")

        StorADE_close()

    logging.info("SSL files created")



    logging.info("Trying to start StatusThread...")

    st = StatusThread(ADEHOST, ADESSLPORT, STATUS_INTERVAL)

    st.start()

    if not st.is_alive():
        logging.critical("StatusThread starting error")
        st.stop()
        StorADE_close()

    logging.info("StatusThread started")



    logging.info("Trying to start ServerThread...")

    if Machine.check_adeptio_mn_ip() == 'IPv6':

        s = ServerThread(HOST_V6, PORT_V6, LISTEN, 'IPv6')

    else:

        s = ServerThread(HOST, PORT, LISTEN, 'IPv4')

    s.start()

    if not s.is_alive():
        logging.critical("ServerThread starting error")
        s.stop()
        StorADE_close()

    logging.info("ServerThread started")



    if '--terminal' in sys.argv:

        raw_input("Press any key to stop the server now...\n")

        logging.info("Trying to stop...")

        st.stop()

        s.stop()

        StorADE_close()