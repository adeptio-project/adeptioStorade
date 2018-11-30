#:: Adeptio Dev team
#:: 2018-11-30
#:: adeptioStorade service core
#:: Alpha testing v2.2

import socket
from time import time

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

tstart_time = time()

#-----------------

start_prep_time = time()

HOST = ''
PORT = 9079
ADDR = (HOST,PORT)
BUFSIZE = 16384
length = 0

end_prep_time = time()

#-----------------

start_socket_time = time()

serv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#serv.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)

serv.bind(ADDR)
serv.listen(5)
#serv.settimeout(2)

end_socket_time = time()

#-----------------

recv_time = 0
write_time = 0

print 'listening ...'

tend_time = time()

total_time = tend_time-tstart_time

while True:

  conn, addr = serv.accept()

  start_time = time()

  print 'client connected ... ', addr

  #-----------------

  start_open_time = time()

  myfile = open('testfile.mov', 'w')

  end_open_time = time()

  #-----------------

  while True:

  	#-----------------

    start_recv_time = time()

    data = conn.recv(BUFSIZE)

    length += len(data)

    end_recv_time = time()

    recv_time += end_recv_time-start_recv_time

  	#-----------------

    if not data: break

  	#-----------------

    start_write_time = time()

    myfile.write(data)

    end_write_time = time()

    write_time += end_write_time-start_write_time

  	#-----------------

  #-----------------

  start_fclose_time = time()

  myfile.close()

  end_fclose_time = time()

  #-----------------


  print 'finished writing file'

  #-----------------

  start_close_time = time()

  conn.close()

  end_close_time = time()

  #-----------------

  length = length/1000/1000
  prep_time = round(end_prep_time-start_prep_time,4)
  socket_time = round(end_socket_time-start_socket_time,4)
  open_time = round(end_open_time-start_open_time,4)
  fclose_time = round(end_fclose_time-start_fclose_time,4)
  close_time = round(end_close_time-start_close_time,4)
  sum_time = prep_time+socket_time+open_time+recv_time+write_time+fclose_time+close_time

  end_time = time()
  total_time = end_time-start_time

  print bcolors.WARNING + 'Program preparing time: ' + bcolors.ENDC, prep_time, 's'
  print bcolors.WARNING + 'File close time: ' + bcolors.ENDC, fclose_time, 's'
  print bcolors.WARNING + 'File open time: ' + bcolors.ENDC, open_time, 's'
  print bcolors.WARNING + 'Socket closing time: ' + bcolors.ENDC, close_time, 's'
  print bcolors.WARNING + 'Socket opening time: ' + bcolors.ENDC, socket_time, 's'
  print bcolors.WARNING + 'File recv time: ' + bcolors.ENDC, recv_time, 's'
  print bcolors.WARNING + 'File write time: ' + bcolors.ENDC, write_time, 's'

  print bcolors.OKBLUE + 'Sum time: ' + bcolors.ENDC, sum_time, 's'
  print bcolors.OKBLUE + 'Total time: ' + bcolors.ENDC, round(total_time,4), 's'

  print bcolors.OKGREEN + 'Length: ' + bcolors.ENDC, length, 'MB'
  print bcolors.OKGREEN + 'Speed: ' + bcolors.ENDC, round(length/total_time,2), 'MB/s'

  recv_time = 0
  write_time = 0

  print '---'
  print '---'

print 'client disconnected'
