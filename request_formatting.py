from urlparse import parse_qs
from urllib import urlencode
import struct
import base64

class RequestFormatting():

    def _split_data(self, size, data):
        r = None
        d = ''

        if len(data) >= size:
            r = data[:size]
            d = data[size:]

        return (r, d)

    def _get_method(self, data):
        r, d = self._split_data(4, data)

        if r is not None:
            r = r.strip(" \t\r\n\x00")

        return (r, d)

    def _set_method(self, method):
        return method + "\x00" * (4-len(method))

    def _get_auth(self, data):
        return self._split_data(16, data)

    def _set_auth(self, key=''):
        return key + "\x00" * (16-len(key))

    def _get_data_size(self, data):
        r, d = self._split_data(4, data)

        if r is not None:
            r = int(struct.unpack('I',r)[0])
            if r == 1651663172:
                r = None

        return (r, d)

    def _set_data_size(self, data):
        return struct.pack('I',len(data))

    def parse_data(self, data):
        if "=" in data:
            return self._parse_query(data)
        return {}

    def str_encode(self, text, key):
        enc = []
        for i in range(len(text)):
            key_c = key[i % len(key)]
            enc_c = chr((ord(text[i]) + ord(key_c)) % 256)
            enc.append(enc_c)
        return base64.urlsafe_b64encode("".join(enc))

    def str_decode(self, text, key):
        dec = []
        try:
            text = base64.urlsafe_b64decode(text)
        except:
            text = ''
        for i in range(len(text)):
            key_c = key[i % len(key)]
            dec_c = chr((256 + ord(text[i]) - ord(key_c)) % 256)
            dec.append(dec_c)
        return "".join(dec)

    def _parse_query(self, data):
        return dict( (k, v if len(v)>1 else v[0] ) 
           for k, v in parse_qs(data).iteritems() )

    def make_query(self, data):
        if type(data) == str:
            return data
        return urlencode(data)

    def parse_header(self, data):
        method, data = self._get_method(data)
        auth, data = self._get_auth(data)
        size, data = self._get_data_size(data)

        return (method, auth, size)

    def parse_request(self, data):
        method, auth, size = self.parse_header(data[:24])
        data = self.parse_data(data[24:])

        return (method, auth, size, data)

    def make_request(self, method, data, binary = ''):
        data = self.make_query(data)
        return self._set_method(method) + self._set_auth('') + self._set_data_size(data + binary) + data + str(binary)