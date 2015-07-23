'''
Maria Martinez
CS 4560 - Operating Systems (Summer '15)
Assignment 03 - Process Synchronization

Purpose: 2 threads write to and read from buffer as 
		 input file is read from and output file is written to

Script syntax is:
	python process_sync.py in_file out_file n m
		in_file 	= file to read from
		out_file 	= file to write to
		n 			= max # of bytes @ each iteration
		m 			= size of buffer in bytes
'''

import sys
import threading
import logging
from random import randint
from Queue import Queue, Full, Empty

logging.basicConfig(level=logging.DEBUG, format= '[%(levelname)s] (%(threadName)-10s) %(message)s',)
q = Queue()

def set_q(buffer_size):
	global q 					# needed to modify global copy of q
	q = Queue(buffer_size)

def run():
	args = sys.argv					# get command line arguments
	file_in = args[1]				# file to read from
	file_out = args[2]				# file to write to
	n = int(args[3])				# n = max # of bytes @ ea. iteration
	m = int(args[4])				# m = size of buffer in bytes

	logging.debug("in: %s, out: %s", file_in, file_out)
	
	set_q(m)						# setup queue with given buffer size
	e = threading.Event()			# event listener for producer completion

	p_thread = threading.Thread(name='t_producer', target=produce, args=(file_in, n, e))
	c_thread = threading.Thread(name='t_consumer', target=consume, args=(file_out, n, e))
	
	p_thread.start()
	c_thread.start()

def produce(in_file, max_bytes, t_event):
	# read from file, store in buffer
	# until end of file
	producer_file = open(in_file, "r")
	end_of_file = False
	while not t_event.isSet():
		buffer_bytes = randint(1, max_bytes) 				# randomly generate buff size to read
		current_bytes = producer_file.read(buffer_bytes)
		if current_bytes == '':
			end_of_file = True
			t_event.set()
			logging.debug('t_event set')					
			break
		try:
			q.put(current_bytes)
			logging.debug('buffer write')					
		except Full:
			logging.debug('buffer full')					
			break											# not enough space, go to next iteration
	
	# done. close file	
	if end_of_file:
		producer_file.close()
		logging.debug('\n*** reading done ***\n')			

def consume(out_file, max_bytes, t_event):
	# read bytes from buffer and write to file
	# keep iterating until event is set
	consumer_file = open(out_file, "w+")
	while not t_event.isSet():
		logging.debug('t_event not yet set')				
		buffer_bytes = randint(1, max_bytes)				# randcomly generate buff size to read
		try:
			current_bytes = q.get()
			string_bytes = str(current_bytes)
			logging.debug('buffer read')					
			consumer_file.write(string_bytes)				# try to get current byte
			q.task_done()									# processing done on this byte
		except Empty:
			logging.debug('buffer empty')					
			break											# not enough unread items, go to next iteration
		
	# event set and queue is not empty?
	# get everything from buffer to finish writing file
	while not q.empty():
		logging.debug('writing reamining buffer')			
		try:
			current_bytes = q.get()
			string_bytes = str(current_bytes)
			logging.debug('buffer read')					
			consumer_file.write(string_bytes)
			q.task_done()
		except Empty:
			logging.debug('reamining buffer empty')			
			break

	# done. close file
	if t_event.isSet() and q.empty():								
		consumer_file.close()
		logging.debug('\n*** writing done ***\n')			

run()
