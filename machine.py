#!/usr/bin/env python
#:: By adeptio (ADE) developers
#:: 2018-12-10
#:: v1.0
#:: storADE part of system

import os
import sys
import platform
import subprocess
import multiprocessing

class Machine():

    #def get_adeptio_daemon():
    #    pid = subprocess.check_output("adepid=$(pgrep adeptiod) ; ls -l /proc/$adepid/exe | awk '{print $11}'", shell=True)
    #    return str(pid)
    #    if pid > 0:
    #        return os.system('readlink -f /proc/'+str(pid)+'/exe')

    def get_adeptio_mn_status_check(self):
        mnstatus_check_tmp = subprocess.check_output("/usr/bin/adeptio-cli masternode status 2> /dev/null | grep pubkey | awk '{print $3}' | cut -c2- | head -c 34", shell=True)
        mnstatus_check = subprocess.check_output("/usr/bin/adeptio-cli masternode list full | grep -c '" + str(mnstatus_check_tmp) + "'", shell=True)
        if int(mnstatus_check) != 1:
            return ("FAILED - status check output "+ str(mnstatus_check) +"")
        else:
            return ("SUCCESS - masternode found in blockchain network")

    #def get_adeptio_machine_ip():
    #    machine_external_ip = os.system("hostname --ip-address | awk '{print $1}'")

    def get_clients_list_file_name(self):
        return "storADE_client_list.json"

    def get_clients_list(self):
        command = "/usr/bin/adeptio-cli masternode list full > " + get_clients_list_file_name()
        os.system(command)
        if os.path.exists("storADE_client_list.json") and os.path.getsize("storADE_client_list.json") > 0:
            return ("SUCCESS - exist and non-empty")
        else:
            return ("FAILED - false")

    def get_machine_storage(self, type=None):
        r = os.statvfs(self.full_path())
        if type == 'free':
            #return r.f_bfree*r.f_frsize
            return r.f_bavail*r.f_frsize
        else:
            return r.f_blocks*r.f_frsize

    def get_machine_memory(self, type=None):
        if type == 'free':
            return os.sysconf('SC_PAGE_SIZE') * os.sysconf('SC_AVPHYS_PAGES')
        else:
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
        }
