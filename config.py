NAME = 'Adeptio StorADE'

HOST = ''
PORT = 9079
HOST_V6 = '::'
PORT_V6 = 9079
LISTEN = 5
ADEHOST = 'storadestats.adeptio.cc'
ADEPORT = 9000
ADESSLPORT = 9001

SIZE = 10737418240
RESERVED_SIZE = 2147483648 #1073741824
SIZE_LIMIT = 2147483648
BUFSIZE = 16384 #8192
CLIENT_TIMEOUT = 2
LOOP_TIMEOUT = 2.0
STATUS_INTERVAL = 3600
DEBUG = False #TEST-----

PATH = 'storage'
SSL_PATH = 'ssl'
ADEPTIO_PATH = '/usr/bin/adeptio-cli'

STORADE_CERTFILE = "storade_server.crt"
STORADE_KEYFILE = "storade_private.key"
STATUS_CERTFILE = "status_server.crt"
STATUS_KEYFILE = "status_private.key"
CLIENTS_FILE = "storADE_client_list.json"
AUTH_FILE = "auth.dat"
LOG_FILE = "storADE.log"