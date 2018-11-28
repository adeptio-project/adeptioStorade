import socket
from time import time

tstart_time = time()

#-----------------

start_prep_time = time()

HOST = ''
PORT = 9876
ADDR = (HOST,PORT)
BUFSIZE = 4096

end_prep_time = time()

#-----------------

start_socket_time = time()

serv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#serv.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)

serv.bind(ADDR)
serv.listen(5)

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

  prep_time = end_prep_time-start_prep_time
  socket_time = end_socket_time-start_socket_time
  open_time = end_open_time-start_open_time
  fclose_time = end_fclose_time-start_fclose_time
  close_time = end_close_time-start_close_time

  print 'Program preparing time: ', prep_time
  print 'Socket opening time: ', socket_time
  print 'File open time: ', open_time
  print 'File recv time: ', recv_time
  print 'File write time: ', write_time
  print 'File close time: ', fclose_time
  print 'Socket closing time: ', close_time

  end_time = time()

  print 'Sum time: ', prep_time+socket_time+open_time+recv_time+write_time+fclose_time+close_time
  print 'Total time: ', total_time+end_time-start_time

  recv_time = 0
  write_time = 0

  print '---'

print 'client disconnected'