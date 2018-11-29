import socket
from time import time, sleep

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

start_time = time()

#-----------------

start_prep_time = time()
HOST = 'localhost'
HOST = '89.47.163.190'

HOST = '192.168.0.100'
HOST = '10.10.10.103'
PORT = 9876
ADDR = (HOST,PORT)
BUFSIZE = 16384
length = 0

videofile = "videos/vsshort-vorbis-ar-1.33.mkv"
videofile = "videos/ffmpeg-20181116-fc94e97-win64-static.zip"
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
read_time = 0
send_time = 0

with open(videofile) as infile:
    while True:
        # Read 430byte chunks of the image
        start_read_time = time()
        chunk = infile.read(BUFSIZE)
        end_read_time = time()
        read_time += end_read_time-start_read_time
        if not chunk: break

        #print len(chunk)
        start_send_time = time()
        client.send(chunk)
        end_send_time = time()
        send_time += end_send_time-start_send_time

"""
#-----------------

start_send_time = time()

length += len(bytes)



client.send(bytes)

end_send_time = time()

#-----------------

start_close_time = time()

client.close()

end_close_time = time()

#-----------------

length = length/1000/1000
prep_time = round(end_prep_time-start_prep_time,4)
socket_time = round(end_socket_time-start_socket_time,4)
read_time = round(end_read_time-start_read_time,4)
send_time = round(end_send_time-start_send_time,4)
close_time = round(end_close_time-start_close_time,4)
sum_time = prep_time+socket_time+read_time+send_time+close_time

end_time = time()

total_time = end_time-start_time

print bcolors.WARNING + 'Program preparing time: ' + bcolors.ENDC, prep_time, 's'
print bcolors.WARNING + 'Socket closing time: ' + bcolors.ENDC, close_time, 's'
print bcolors.WARNING + 'Socket opening time: ' + bcolors.ENDC, socket_time, 's'
print bcolors.WARNING + 'File read time: ' + bcolors.ENDC, read_time, 's'
print bcolors.BOLD + 'File send time: ' + bcolors.ENDC, send_time, 's'

print bcolors.OKBLUE + 'Sum time: ' + bcolors.ENDC, sum_time, 's'
print bcolors.OKBLUE + 'Total time: ' + bcolors.ENDC, round(total_time,4), 's'

print bcolors.OKGREEN + 'Length: ' + bcolors.ENDC, length, 'MB'
print bcolors.OKGREEN + 'Speed: ' + bcolors.ENDC, round(length/total_time,2), 'MB/s'