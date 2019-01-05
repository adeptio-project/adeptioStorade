import time
import logging

from config import *
from auth import Auth
from files import Files
from machine import Machine
from request_formatting import RequestFormatting

class Do(Auth, RequestFormatting, Files, Machine):

    def __init__(self, addr):
        self.cmd = None
        self.data = ''
        self.in_buffer = ''
        self.out_buffer = ''
        self.called_cmd = []
        self.parsed_data = {}
        self.timeout = None
        self.checking = False
        self.correct_request = False
        self.file = {'status':False,'fname':False,'seek':0,'done':False}
        self.do_list = self._get_func_list('do_')
        self.close_when_done = False
        self.client_ip, self.client_port = addr
        self.client_name = str(self.client_ip) + ":" + str(self.client_port)

    def _get_func_list(self, prefix):
        r = []
        for n in dir(self):
            if n.startswith(prefix):
                r.append(n[len(prefix):])
        return r

    def _exist_cmd(self, cmd):
        return cmd in self.do_list

    def _need_auth(self, method):
        return method not in ('INFO')

    def _need_data(self, method):
        return method not in ('INFO','STAT', 'LIST')

    def _just_once(self, method):
        return method not in ('FILE')

    def _call_cmd(self, cmd):
        mname = 'do_' + str(cmd)

        if not hasattr(self, mname):
            return

        method = getattr(self, mname)

        self.called_cmd.append(str(cmd))

        method()

    def _format_data(self, data):
        new_req_data = ''

        if not self._need_data(self.cmd):

            data = ''

        if len(data) > self.size:

            new_req_data = data[self.size:]
            data = data[:self.size]

        self.size -= len(data)

        return data, new_req_data

    def _check_request(self, data, s = 24):
        if self.in_buffer is None: return ('',None)

        self.in_buffer += data

        cmd, auth, size = self.parse_header(self.in_buffer[:s])

        if cmd is None:

            return ('',None) #wait more data

        if not self._exist_cmd(cmd):

            return ('','Incorrect Command') #close socket

        if self._need_auth(cmd):

            if auth is None:

                return ('',None) #wait more data

            if not self.check_auth(auth):
                
                return ('','Incorrect Authentication') #close socket

        if self._need_data(cmd):

            if size is None:

                return ('',None) #wait more data

            if size <= 0:

                return ('','Incorrect Size') #close socket

        r = self.in_buffer[s:]
        self.cmd = cmd
        self.auth = auth
        self.size = 0 if size is None else size
        self.in_buffer = ''
        self.correct_request = True
        self.checking = False

        return r, None

    def request(self, data):
        if self.in_buffer is None: 
            return

        if self.checking: 
            self.request(data)
            return

        if not self.correct_request:

            self.checking = True

            data, error = self._check_request(data)

            self.checking = False

            if error is not None: #close socket

                self.in_buffer = None

                self.send(('FAIL', error))

                return

        if not self.correct_request: #We waiting more data

            self.timeout = time.time()

            return

        data, new_req_data = self._format_data(data)

        self.data += data

        if self.size > 0 and self._need_data(self.cmd) and self._just_once(self.cmd): #We waiting more data

            self.timeout = time.time()

            return

        if len(self.data) > 0 and self._just_once(self.cmd):

            self.parsed_data = self.parse_data(self.data)

        if not self._just_once(self.cmd) or self.cmd not in self.called_cmd:

            self._call_cmd(self.cmd)

        if new_req_data:

            self.timeout = time.time()
            return #Turn off for now

            self.correct_request = False

            self.request(new_req_data)


    def send(self, request, close = True):

        if type(request) == tuple:
            binary = ''
            method, data = request
            if type(data) == dict:
                if data.get('file'):
                    binary = "&file=" + self.file_read(data['file'])
                    del data['file']
            request = self.make_request(method, data, binary)

        self.close_when_done = close
        self.out_buffer = self.out_buffer + str(request)

    def do_INFO(self):
        self.send('StorADE')

    def do_STAT(self):
        self.send(('STAT', self.full_info()))

    def do_PUT(self):
        #File name must have lenght limit and symbols limit if file name is incorrect rejected request
        if not self.parsed_data.get('fname'):
            self.send(('FAIL', 'File name is Incorrect'))
            return

        #File size must be integer
        if not self.parsed_data.get('fsize'):
            self.send(('FAIL', 'File size is Incorrect'))
            return

        if isinstance(self.parsed_data['fname'], (list, dict)):
            self.parsed_data['fname'] = self.parsed_data['fname'][0]

        try:
            size = int(self.parsed_data['fsize'])
        except ValueError:
            self.send(('FAIL', 'File size is Incorrect'))
            return

        file = self.parsed_data['fname']
        size = int(self.parsed_data['fsize'])

        if size <= 0:
            self.send(('FAIL', 'File size is Incorrect'))
            return

        if not self.file_name_check(file):
            self.send(('FAIL', 'File name is Incorrect'))
            return

        if self.file_check(file):
            self.send(('FAIL', 'Have file with the same name'))
            return

        if self.get_free_space() <= size:
            self.send(('FAIL', 'Not inife space'))
            return

        if SIZE_LIMIT < size:
            self.send(('FAIL', 'File too big'))
            return

        if self.is_prepared_file(file, 0):
            self.send(('FAIL', 'I am already prepared for this file'))
            return

        if not self.prepare_file(file, size):
            self.send(('FAIL', 'Server error while preparing for new file'))
            return

        #If file will not come in SET time, prepare and appending file must be removed
        #If file is prepared, new PUT request for the same file must be rejected and if it is appending (writing) also must be rejected
        self.send(('INFO', 'I am prepare for ' + str(file) + ' file which size ' + str(size)),False)

    def do_DEL(self):
        if not self.parsed_data.get('fname'):
            self.send(('FAIL', 'File name is Incorrect'))
            return

        file = self.parsed_data['fname']

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
        if not self.parsed_data.get('fname'):
            self.send(('FAIL', 'File name is Incorrect'))
            return

        file = self.parsed_data['fname']

        if not self.file_check(file):
            self.send(('FAIL', 'Don\'t have this file'))
            return

        self.send(('FILE', {'fname': file, 'fsize': self.get_file_size(file), 'file': file}))

    def do_FILE(self):
        if self.file['done']: return

        if not self.parsed_data: #Wait if didn't get enough data

            data = self.data

            self.parsed_data = self.parse_data(data)

            self.data = self.data.replace(data, '')

        if self.file['fname']:  #Close socket if long time didn't get full file and replace to prepeard

            data = self.data
            file = data
            seek = self.file['seek']
            fname = self.file['fname']
            self.data = self.data.replace(data, '')

        else:

            if not self.parsed_data.get('fname'):
                self.send(('FAIL', 'File name is Incorrect'))
                return

            if not self.parsed_data.get('file'): #If file data will be second recv
                self.send(('FAIL', 'No file data found'))
                return

            file = self.parsed_data['file']
            seek = 0
            fname = self.parsed_data['fname']

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