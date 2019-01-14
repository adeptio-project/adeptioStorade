import os
import sys
import platform
import subprocess
import multiprocessing
import json
#import ijson.backends.yajl2 as ijson

from config import *
from files import Files

class Machine(Files):

    def ssl_path(self, file=None, start=PATH):
        return os.path.join(start, SSL_PATH, file) if file != None else os.path.join(start, SSL_PATH)

    def check_adeptio_mn_status(self):
        try:
            status = subprocess.check_output(ADEPTIO_PATH + " masternode status 2> /dev/null | grep pubkey | awk '{print $3}' | cut -c2- | head -c 34", shell=True)
            if status:
                return True
        except:
            pass
        try:
            status = subprocess.check_output(ADEPTIO_PATH + " masternode status 2> /dev/null | grep addr | tail -n -1 | awk '{print $2}' | cut -c2- | head -c 34", shell=True)
            if status:
                return True
        except:
            pass
        return False

    def check_adeptio_mn_list(self):
        try:
            result_count = subprocess.check_output(ADEPTIO_PATH + " masternode list full | wc -l", shell=True)
            if int(result_count) > 5:
                return True
        except:
            pass
        try:
            result_count = subprocess.check_output(ADEPTIO_PATH + " masternode list | wc -l", shell=True)
            if int(result_count) > 5:
                return True
        except:
            pass
        return False

    def get_adeptio_mn_list(self):
        file_name = self.full_path(CLIENTS_FILE)
        old_command = ADEPTIO_PATH + " masternode list full > " + file_name
        new_command = ADEPTIO_PATH + " masternode list > " + file_name
        os.system(old_command)
        if self.file_check(CLIENTS_FILE):
            if len(self.file_read(CLIENTS_FILE)) < 5:
                os.system(new_command)
                return True
        return False

    def create_clients_list(self):
        new_ver = self.get_adeptio_mn_list()
        ips = []
        if self.file_check(CLIENTS_FILE):
            clients = self.file_read(CLIENTS_FILE)
            if clients:
                clients = json.loads(clients)
                if clients:
                    if new_ver:
                        for i in clients:
                            ip = i.get('ip').strip("[]")
                            ips.append(ip)
                    else:
                        for i in clients.values():
                            s = i.split()
                            status, prot, key, ip, st, ts, rt = s
                            ip, separator, port = ip.rpartition(':')
                            ip = ip.strip("[]")
                            ips.append(ip)
        self.file_write(CLIENTS_FILE,str(ips))
        return len(ips)

    def get_clients_list(self):
        if self.file_check(CLIENTS_FILE):
            clients = self.file_read(CLIENTS_FILE)
            return clients
        return []

    def get_machine_storage(self, type=None):
        r = os.statvfs(self.full_path())

        if type == 'free':
            #return r.f_bfree*r.f_frsize
            return r.f_bavail*r.f_frsize

        return r.f_blocks*r.f_frsize

    def get_machine_memory(self, type=None):

        if type == 'free':
            return os.sysconf('SC_PAGE_SIZE') * os.sysconf('SC_AVPHYS_PAGES')

        return os.sysconf('SC_PAGE_SIZE') * os.sysconf('SC_PHYS_PAGES')

    def get_machine_name(self):
        return platform.linux_distribution()

    def get_python_version(self):
        return sys.version

    def get_kernel_version(self):
        return platform.release()

    def get_platform_type(self):
        return platform.machine()

    def get_machine_cpu(self):
        #return os.cpu_count()
        return multiprocessing.cpu_count()

    def get_free_space(self):
        MachineSpaceLeft = self.get_machine_storage('free')
        StorADESpaceLeft = SIZE - self.get_files_size()

        if MachineSpaceLeft < StorADESpaceLeft + RESERVED_SIZE:
            
            StorADESpaceLeft = MachineSpaceLeft - RESERVED_SIZE

        return StorADESpaceLeft

    def valid_ip(self, ip):
        return ip.count('.') == 3 and all(0<=int(num)<256 for num in ip.rstrip().split('.'))

    def local_ip(self, ip):
        if self.valid_ip(ip):
            if ip.startswith('192.168') or ip.startswith('10.') or ip.startswith('127.'):
                return True
        return False

    def get_last_log(self, count = 1):
        if self.file_check(LOG_FILE):
            lines = self.file_read(LOG_FILE,'rt','lines')
            i = len(lines)-int(count) if len(lines) > int(count) else 0
            return lines[i:]
        return False

    def full_info(self):
        return {
            'os': self.get_machine_name(),
            'os_version': self.get_kernel_version(),
            'type': self.get_platform_type(),
            'cpu': self.get_machine_cpu(),
            'python': self.get_python_version(),
            'total_memory': self.get_machine_memory(),
            'free_memory': self.get_machine_memory('free'),
            'total_storage': self.get_machine_storage(),
            'free_storage': self.get_machine_storage('free'),
            'ADE_free_storage': self.get_free_space(),
            'clients_count': self.create_clients_list(),
        }
