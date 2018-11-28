from time import time

start_time = time()

#-----------------

start_prep_time = time()

videofile = "videos/vsshort-vorbis-ar-1.33.mkv"
videofile = "videos/stream_4389697.ts"

end_prep_time = time()

#-----------------

start_read_time = time()

bytes = open(videofile).read()

end_read_time = time()

#-----------------

start_open_time = time()

myfile = open('testfile.mov', 'w')

end_open_time = time()

#-----------------

start_write_time = time()

myfile.write(bytes)

end_write_time = time()

#-----------------

start_fclose_time = time()

myfile.close()

end_fclose_time = time()

#-----------------

prep_time = end_prep_time-start_prep_time
read_time = end_read_time-start_read_time
open_time = end_open_time-start_open_time
write_time = end_write_time-start_write_time
fclose_time = end_fclose_time-start_fclose_time

print 'Program preparing time: ', prep_time
print 'File read time: ', read_time
print 'File open time: ', open_time
print 'File write time: ', write_time
print 'File close time: ', fclose_time

end_time = time()

print 'Sum time: ', prep_time+read_time+open_time+write_time+fclose_time
print 'Total time: ', end_time-start_time