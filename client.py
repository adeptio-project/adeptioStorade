import socket
from time import time

start_time = time()

#-----------------

start_prep_time = time()

HOST = 'localhost'
PORT = 9876
ADDR = (HOST,PORT)
BUFSIZE = 4096
videofile = "videos/vsshort-vorbis-ar-1.33.mkv"
videofile = "videos/stream_4389697.ts"

end_prep_time = time()

#-----------------

start_socket_time = time()

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#client.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
client.connect(ADDR)

end_socket_time = time()

#-----------------

start_read_time = time()

bytes = open(videofile).read()

end_read_time = time()

#-----------------

"""
with open(videofile) as infile:
    while True:
        # Read 430byte chunks of the image
        chunk = infile.read(BUFSIZE)
        if not chunk: break

        print len(chunk)
        client.send(chunk)
"""

#-----------------

start_send_time = time()

client.send(bytes)

end_send_time = time()

#-----------------

start_close_time = time()

client.close()

end_close_time = time()

#-----------------


prep_time = end_prep_time-start_prep_time
socket_time = end_socket_time-start_socket_time
read_time = end_read_time-start_read_time
send_time = end_send_time-start_send_time
close_time = end_close_time-start_close_time

print 'Program preparing time: ', prep_time
print 'Socket opening time: ', socket_time
print 'File read time: ', read_time
print 'File send time: ', send_time
print 'Socket closing time: ', close_time

end_time = time()

print 'Sum time: ', prep_time+socket_time+read_time+send_time+close_time
print 'Total time: ', end_time-start_time