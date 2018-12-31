from OpenSSL import crypto, SSL
from socket import gethostname

from config import *
from files import Files
from machine import Machine

class SSL_(Files):

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

        machine = Machine()

        sade_cert = machine.ssl_path(STORADE_CERTFILE,'')
        sade_key = machine.ssl_path(STORADE_KEYFILE,'')

        stat_cert = machine.ssl_path(STATUS_CERTFILE,'')
        stat_key = machine.ssl_path(STATUS_KEYFILE,'')

        key = self.create_key()
        cert = self.create_cert(key)

        self.file_write(sade_cert, crypto.dump_certificate(crypto.FILETYPE_PEM, cert))
        self.file_write(sade_key, crypto.dump_privatekey(crypto.FILETYPE_PEM, key))

        self.file_write(stat_cert, crypto.dump_certificate(crypto.FILETYPE_PEM, cert))
        self.file_write(stat_key, crypto.dump_privatekey(crypto.FILETYPE_PEM, key))

        if not self.file_check(sade_cert) or not self.file_check(sade_key) or not self.file_check(stat_cert) or not self.file_check(stat_key):

            return False

        return True