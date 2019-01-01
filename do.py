import logging

from config import *
from auth import Auth
from files import Files
from machine import Machine
from request_formatting import RequestFormatting

class Do(Auth, RequestFormatting, Files, Machine):

    def __init__(self, client_name, data):
        self.out_buffer = ''
        self.file = {'status':False,'fname':False,'seek':0,'done':False}
        self.close_when_done = False
        self.client_name = client_name
        self.cmd, self.auth, self.size, data = self.parse_request(data)
        self.request(data)

    def getclientname(self):
        return self.client_name

    def request(self, data):
        self.size -= len(data)
        #Can be finish previous request and start new one: vtgt5GET25H
        self.data = data#self.parse_query(data) if len(data) > 0 else data
        mname = 'do_' + self.cmd

        if not hasattr(self, mname):
            self.send(('FAIL', 'Unsupported method ' + self.cmd))
            return

        method = getattr(self, mname)

        if self.check_auth(self.auth) or self.cmd == 'INFO':
            method()
        else:
            self.send(('FAIL', 'Incorrect Authentication Data'))
            return

    def send(self, request, close = True):

        if type(request) == tuple:
            binary = ''
            method, data = request
            if type(data) == dict:
                if data.get('file'):
                    binary = "&file=" + self.file_read(data['file'])
                    del data['file']
            request = self.make_request(method, data, binary)

        if DEBUG:
           logging.debug('To %s send message: %s', self.getclientname(), request)

        self.close_when_done = close
        self.out_buffer = self.out_buffer + str(request)

    def do_INFO(self):
        self.send('StorADE')

    def do_STAT(self):
        self.send(('STAT', self.full_info()))

    def do_PUT(self):
        #File name must have lenght limit and symbols limit if file name is incorrect rejected request
        if not self.data.get('fname'):
            self.send(('FAIL', 'File name is Incorrect'))
            return

        #File size must be integer
        if not self.data.get('fsize'):
            self.send(('FAIL', 'File size is Incorrect'))
            return

        file = self.data['fname']
        size = int(self.data['fsize'])

        if self.file_check(file):
            self.send(('FAIL', 'Have file with the same name'))
            return

        if self.get_free_space() <= size:
            self.send(('FAIL', 'Not inife space'))
            return

        if SIZE_LIMIT < size:
            self.send(('FAIL', 'File too big'))
            return

        if not self.prepare_file(file, size):
            self.send(('FAIL', 'Server error while preparing for new file'))
            return

        #If file will not come in SET time, prepare and appending file must be removed
        #If file is prepared, new PUT request for the same file must be rejected and if it is appending (writing) also must be rejected
        self.send(('INFO', 'I am prepare for ' + str(file) + ' file which size ' + str(size)),False)

    def do_DEL(self):
        if not self.data.get('fname'):
            self.send(('FAIL', 'File name is Incorrect'))
            return

        file = self.data['fname']

        if not self.file_check(file,0):
            self.send(('FAIL', 'No removable file found'))
            return

        if not self.remove_file(file):
            self.send(('FAIL', 'Can\'t remove file'))
            return

        self.send(('INFO', 'File remove success'))

    def do_LIST(self):
        files = self.get_files_list()

        if not files:
            self.send(('FAIL', 'No files found'))
            return

        self.send(('LIST', {'fname': files}))

    def do_GET(self):
        if not self.data.get('fname'):
            self.send(('FAIL', 'File name is Incorrect'))
            return

        file = self.data['fname']

        if not self.file_check(file):
            self.send(('FAIL', 'Don\'t have this file'))
            return

        self.send(('FILE', {'fname': file, 'fsize': self.get_file_size(file), 'file': file}))

    def do_FILE(self):

        if self.file['fname']:

            file = self.data
            seek = self.file['seek']
            fname = self.file['fname']

        elif not type(self.data) == str:
        #else:

            #self.data can't be string
            if not self.data.get('fname'):
                self.send(('FAIL', 'File name is Incorrect'))
                return

            if not self.data.get('file'):
                self.send(('FAIL', 'No file data found'))
                return

            seek = 0
            file = self.data['file']
            fname = self.data['fname']

        elif not self.file['done']:

            self.send(('FAIL', 'Don\'t reognize data'))
            return
        else:
            return

        size = len(file)

        #If file content lenght more than prepared file, don't fail just save less data
        if not self.is_prepared_file(fname, size):
            self.send(('FAIL', 'I am not prepare for this file'))
            return

        self.file['seek'] = seek + size
        self.file['fname'] = fname
        self.file['status'] = self.append_file(fname, file, seek)

        status = self.file['status']

        if not self.file['status'] == 'WAIT':
            self.file = {'status':False,'fname':False,'seek':0,'done':True}

        if status == 'FAIL':
            self.send(('FAIL', 'Server error while writing new file'))

        if status == 'DONE':
            self.send(('INFO', 'Files saved success'))