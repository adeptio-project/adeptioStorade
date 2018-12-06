#!/usr/bin/env python
#:: By adeptio (ADE) developers
#:: 2018-12-05
#:: v1.0
#:: storADE machine info collector

import os
import sys
import errno
import platform
import socket
import subprocess
import multiprocessing

#def get_adeptio_daemon():
#    pid = subprocess.check_output("adepid=$(pgrep adeptiod) ; ls -l /proc/$adepid/exe | awk '{print $11}'", shell=True)
#    return str(pid)
#    if pid > 0:
#        return os.system('readlink -f /proc/'+str(pid)+'/exe')

def get_adeptio_mn_status_check():
    mnstatus_check_tmp = subprocess.check_output("/usr/bin/adeptio-cli masternode status 2> /dev/null | grep pubkey | awk '{print $3}' | cut -c2- | head -c 34", shell=True)
    mnstatus_check = subprocess.check_output("/usr/bin/adeptio-cli masternode list full | grep -c '" + str(mnstatus_check_tmp) + "'", shell=True)
    if mnstatus_check != 1:
        return ("FAILED - status check output: "+ str(mnstatus_check) +"")
    else:
        return ("SUCCESS - status check output: "+ str(mnstatus_check) +"")

#def get_adeptio_machine_ip():
#    machine_external_ip = os.system("hostname --ip-address | awk '{print $1}'")

def get_clients_list_file_name():
    return "storADE_client_list.json"

def get_clients_list():
    command = "/usr/bin/adeptio-cli masternode list full > " + get_clients_list_file_name()
    os.system(command)
    if os.path.exists("storADE_client_list.json") and os.path.getsize("storADE_client_list.json") > 0:
        return ("SUCCESS - exist and non-empty")
    else:
        return ("FAILED - false")

def get_machine_storage(loc='/',type=None):
    r = os.statvfs(loc)
    if type == 'free':
        #return r.f_bfree*r.f_frsize
        return r.f_bavail*r.f_frsize
    else:
        return r.f_blocks*r.f_frsize

def get_machine_memory(type=None):
    if type == 'free':
        return os.sysconf('SC_PAGE_SIZE') * os.sysconf('SC_AVPHYS_PAGES')
    else:
        return os.sysconf('SC_PAGE_SIZE') * os.sysconf('SC_PHYS_PAGES')

def get_machine_name():
    return platform.system()

def get_python_version():
    return sys.version

def get_kernel_version():
    return platform.release()

def get_platform_type():
    return platform.machine()

def get_machine_cpu():
    #return os.cpu_count()
    return multiprocessing.cpu_count()

def b_to_g(i,r=0):
    return round(float(i)/(1024.**3),r)

print 'OS: ', get_machine_name()
print 'OS kernel version: ', get_kernel_version()
print 'OS platform type: ', get_platform_type()
print 'Python version: ', get_python_version()
print 'CPU count: ', get_machine_cpu()
print 'Memory: ', b_to_g(get_machine_memory(),2), 'GB'
print 'Free Memory: ', b_to_g(get_machine_memory('free'),2), 'GB'
print 'Free storage space: ', b_to_g(get_machine_storage('videos','free'),2), 'GB'
print 'Is Adeptio client list file exist?: ', get_clients_list() 
print 'Adeptio masternode validation check:', get_adeptio_mn_status_check()
