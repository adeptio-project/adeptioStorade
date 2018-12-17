from urlparse import parse_qs
from urllib import urlencode
import struct
import base64

class RequestFormatting():

    def _get_method(self, data):
        if len(data) >= 4:
            return data[:4].strip(" \t\r\n\x00")
        return data

    def _set_method(self, method):
        return method + "\x00" * (4-len(method))

    def _get_auth(self, data):
        if len(data) >= 20:
            return data[4:20]
        return ''

    def _set_auth(self, key=''):
        return key + "\x00" * (16-len(key))

    def _get_data_size(self, data):
        if len(data) >= 24:
            return int(struct.unpack('I',data[20:24])[0])
        return 0

    def _set_data_size(self, data):
        return struct.pack('I',len(data))

    def _get_data(self, data):
        if len(data) > 24:
            data = data[24:]
            if "=" in data:
                return self.parse_query(data)
            return data
        return {}

    def str_encode(self, text, key):
        enc = []
        for i in range(len(clear)):
            key_c = key[i % len(key)]
            enc_c = chr((ord(clear[i]) + ord(key_c)) % 256)
            enc.append(enc_c)
        return base64.urlsafe_b64encode("".join(enc))

    def str_decode(self, text, key):
        dec = []
        enc = base64.urlsafe_b64decode(enc)
        for i in range(len(enc)):
            key_c = key[i % len(key)]
            dec_c = chr((256 + ord(enc[i]) - ord(key_c)) % 256)
            dec.append(dec_c)
        return "".join(dec)

    def parse_query(self, data):
        return dict( (k, v if len(v)>1 else v[0] ) 
           for k, v in parse_qs(data).iteritems() )

    def make_query(self, data):
        if type(data) == str:
            return data
        return urlencode(data)

    def parse_request(self, data):
        return (self._get_method(data), self._get_auth(data), self._get_data_size(data), self._get_data(data))

    def make_request(self, method, data, binary = ''):
        data = self.make_query(data)
        return self._set_method(method) + self._set_auth('') + self._set_data_size(data + binary) + data + str(binary)