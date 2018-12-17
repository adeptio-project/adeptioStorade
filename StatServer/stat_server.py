import threading
import asyncore
import logging
import ssl
import sys
import os

from socket import gethostname

from config import *

def ssl_path(file=None, start=PATH):
    return os.path.join(start, SSL_PATH, file) if file != None else os.path.join(start, SSL_PATH)

def full_path(file=None):
    return os.path.join(PATH, file) if file != None else PATH

def _path_exist(path):
    return os.path.exists(path)

def _make_dir(dir):
    return os.makedirs(dir)

def _is_file(file):
    return os.path.isfile(file)

def _get_size(file):
    return os.path.getsize(file)

def file_check(file, size = 1):
    file_path = full_path(file)

    if self._is_file(file_path):

        if self._get_size(file_path) >= int(size):

            return True

    return False

def dir_check(path):

    if not _path_exist(path):

        _make_dir(path)

    return _path_exist(path)

def file_write(file, data, type='wt', seek=None): #w-write, a-append, t-text, b-binary

    try:
        with io.open(full_path(file), type) as f:

            if not seek == None:
                f.seek(int(seek))

            f.write(unicode(data))

        return True

    except IOError as e:

        return False

class SSL_():

    def create_key(self):

        # create a key pair
        key = crypto.PKey()
        key.generate_key(crypto.TYPE_RSA, 4096)

        return key

    def create_cert(self, key):

        # create a self-signed cert
        cert = crypto.X509()
        cert.get_subject().C = "EU"
        cert.get_subject().ST = "London"
        cert.get_subject().L = "London"
        cert.get_subject().O = NAME
        cert.get_subject().OU = NAME
        cert.get_subject().CN = gethostname()
        cert.set_serial_number(1000)
        cert.gmtime_adj_notBefore(0)
        cert.gmtime_adj_notAfter(10*365*24*60*60)
        cert.set_issuer(cert.get_subject())
        cert.set_pubkey(key)
        cert.sign(key, 'sha1')

        return cert

    def create_ssl_files(self):

        stat_cert = ssl_path(STAT_CERTFILE,'')
        stat_key = ssl_path(STAT_KEYFILE,'')

        key = self.create_key()
        cert = self.create_cert(key)

        file_write(stat_cert, crypto.dump_certificate(crypto.FILETYPE_PEM, cert))
        file_write(stat_key, crypto.dump_privatekey(crypto.FILETYPE_PEM, key))

        if not file_check(stat_cert) or not file_check(stat_key):

            return False

        return True

class StorADE(asyncore.dispatcher_with_send):

    buffer_out = ''
    close_when_done = False
    get_data = 0
    send_data = 0

    def read_storADE_message(self, data):

        self.buffer_out += ''
        self.close_when_done = True

    def getclientname(self):

        ip, port = self.getpeername()

        return ip + ":" + str(port)

    def handle_close(self):

        if DEBUG:
            logging.info('Disconnected from %s client from which got %i bytes and send %i bytes', self.getclientname(), self.get_data, self.send_data)

        self.close()

    def handle_read(self):

        data = self.recv(BUFSIZE)

        if data:

            if DEBUG:
               logging.debug('From %s got message: %s', self.getclientname(), data)

            self.get_data += len(data)

            self.read_storADE_message(data)

            if DEBUG:
               logging.info('Get %i bytes data from %s client', len(data), self.getclientname())

    def writable(self):
        return (not self.connected) or len(self.buffer_out)

    def handle_write(self):

        if DEBUG:
            logging.info('Sending data to %s client', self.getclientname())

        self.send_data += len(self.buffer_out)
        self.send(self.buffer_out)

        self.buffer_out = self.out_buffer

        if self.close_when_done and self.out_buffer == '':

            self.handle_close()
            
            self.close_when_done = False

class Server(asyncore.dispatcher):

    def __init__(self, host, port, listen):
        asyncore.dispatcher.__init__(self)
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        #self.create_socket(socket.AF_INET6, socket.SOCK_STREAM) #IPv6
        #self.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
        self.set_reuse_addr() # try to re-use a server port if possible
        self.bind((host, port))
        self.listen(listen)
        self.port = port
        logging.info("Stat Server is ready and listening on %i port", self.port)

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

            sock = ssl.wrap_socket(sock, server_side=True, certfile=ssl_path(STORADE_CERTFILE), keyfile=ssl_path(STORADE_KEYFILE)) #ssl_version=PROTOCOL_TLS, ca_certs=None

            StorADE(sock) #Send accepted client to Client function!

    def handle_close(self):

        logging.info('Stat Server is closing on %i port', self.port)

        self.close()

    def allow_client(self, addr):
        ip, port = addr
        return True

class StatServerThread(threading.Thread):
    def __init__(self, host, port, listen):
        threading.Thread.__init__(self)
        self.server = Server(host, port, listen)

    def run(self):
        asyncore.loop()

    def stop(self):
        asyncore.close_all()
        self.server.close()
        self.join()

def StatServer_close():
    logging.info("Stat Server closed")
    logging.shutdown()
    sys.exit()

if __name__ == "__main__":

    dir_check(full_path())

    logging.basicConfig(filename=full_path(LOG_FILE), level=logging.DEBUG, format='%(asctime)s | %(levelname)s | %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

    logging.getLogger().addHandler(logging.StreamHandler())

    logging.info("Stat Server started")

    try:

        __import__('OpenSSL')

    except ImportError:

        logging.critical("ImportError: No module named OpenSSL")

        StatServer_close()

    if not dir_check(full_path()):

        logging.critical("Can't create Stat Server folder")

        StatServer_close()

    if not dir_check(ssl_path()):

        logging.critical("Can't create SSL folder")

        StatServer_close()

    logging.info("Trying to create ssl files...")

    from OpenSSL import crypto, SSL

    if not SSL_().create_ssl_files():

        logging.critical("Failure creating ssl files")

        StatServer_close()

    logging.info("SSL files created")

    logging.info("Trying to start StatServerThread...")

    s = StatServerThread(HOST, PORT, LISTEN)

    s.start()

    if not s.is_alive():
        logging.critical("StatServerThread starting error")
        s.stop()
        StatServer_close()

    logging.info("StatServerThread started")

    raw_input("Press any key to stop the server now...\n")

    logging.info("Trying to stop StatServerThread...")

    s.stop()

    StatServer_close()