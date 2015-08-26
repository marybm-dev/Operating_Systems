'''
Maria Martinez
CS 4560 - Operating Systems (Summer '15)
Assignment 06 - Virtual Memory

Purpose: Simulation of virtual memory management 
		 with Least-Recently-Used (LRU) algorithm
'''

import time

# @param r_bit = page is being referenced
# @param m_bit = dirty bit (has been modified)
# @param v_bit = valid/invalid bit
# @param frame = number of frame being used
# @param duration = clock ticks given 
# @param t_stamp = latest time stamp
class Page(object):
	def __init__(self, r_bit = 0, m_bit = 0, v_bit = 0, frame = 0, duration = 0, t_stamp = time.time()):
		self.r_bit = r_bit
		self.m_bit = m_bit
		self.v_bit = v_bit
		self.frame = frame
		self.duration = duration
		self.t_stamp = t_stamp

	def __str__(self):
		return "%s %s %s %s     duration: %s" % (self.r_bit, self.m_bit, self.v_bit, self.frame, self.duration)

def get_lru(page_table):
	index = 0
	victim = page_table[0]
	lru_time = page_table[0].t_stamp
	for i, page in enumerate(page_table):
		if page.t_stamp > lru_time:
			lru_time = page.t_stamp
			victim = page
	victim.v_bit = 0
	victim.t_stamp = time.time()
	return index

def main():
	# get input from user: page ref, red or write (m_bit), 
	print 'Enter # of Virtual Pages'
	pages = int(raw_input('> '))
	print 'Enter # of available Page Frames'
	frames = int(raw_input('> '))
	print 'Enter # of References'
	references = int(raw_input('> '))

	references_array = []
	for i in range(0,references+1):
		print 'Enter Page Referenced, Read or Write (0 or 1), and Duration'
		curr_ref = raw_input('> ')
		references_array.append(curr_ref)
	references_array.sort()
	
	# add pages to table and display
	print "\nPage Table\n"
	page_table = []	
	index_counter = 0
	for index in range(0, pages):
		if index_counter < len(references_array) and index == int(references_array[index_counter][0]):
			curr_page = Page(r_bit = 1, m_bit=int(references_array[index_counter][1]), v_bit = 1, frame = index_counter, duration=int(references_array[index_counter][2]))
			index_counter += 1
		else:
			curr_page = Page()
		print " ", curr_page
		page_table.append(curr_page)
	print "\n"

	size = len(page_table)

	clock_ticks = 0
	array_index = 0
	faults = 0
	for i in range(0, 25):
		if array_index == size:
			array_index = 0

		page = page_table[array_index]

		if page.duration == 0:
			print "i", i, "      page", array_index, "     r_bit", page.r_bit, "     v_bit", page.v_bit, "      duration", page.duration

		while page.duration > 0:
			print "i", i, "      page", array_index, "     r_bit", page.r_bit, "     v_bit", page.v_bit, "      duration", page.duration
			# page fault, this page is not being referenced
			if page.v_bit == 1 and page.r_bit == 0:
				victim = get_lru(page_table)
				page.r_bit = 1
				faults += 1
				print "Fault: page", victim, "evicted,", i, "brought into memory."
			# page invalidated when it was a prior victim
			elif page.v_bit == 0:
				faults += 1
				print "Fault: no page evicted, page", i, "brought into memory."

			page.duration -= 1
			clock_ticks += 1

			if clock_ticks == 6:
				clock_ticks = 0
				page.r_bit = 0
				print " *** 6 clock ticks - current r_bit set to 0 *** "
				break

		array_index += 1

	print "\nTotal number of faults is", faults

main()



'''
*** SAMPLE INPUT / OUTPUT ***


Enter # of Virtual Pages
> 5
Enter # of available Page Frames
> 4
Enter # of References
> 3
Enter Page Referenced, Read or Write (0 or 1), and Duration
> 007
Enter Page Referenced, Read or Write (0 or 1), and Duration
> 419
Enter Page Referenced, Read or Write (0 or 1), and Duration
> 218
Enter Page Referenced, Read or Write (0 or 1), and Duration
> 303

Page Table

  1 0 1 0     duration: 7
  0 0 0 0     duration: 0
  1 1 1 1     duration: 8
  1 0 1 2     duration: 3
  1 1 1 3     duration: 9


i 0       page 0      r_bit 1      v_bit 1       duration 7
i 0       page 0      r_bit 1      v_bit 1       duration 6
i 0       page 0      r_bit 1      v_bit 1       duration 5
i 0       page 0      r_bit 1      v_bit 1       duration 4
i 0       page 0      r_bit 1      v_bit 1       duration 3
i 0       page 0      r_bit 1      v_bit 1       duration 2
 *** 6 clock ticks - current r_bit set to 0 *** 
i 1       page 1      r_bit 0      v_bit 0       duration 0
i 2       page 2      r_bit 1      v_bit 1       duration 8
i 2       page 2      r_bit 1      v_bit 1       duration 7
i 2       page 2      r_bit 1      v_bit 1       duration 6
i 2       page 2      r_bit 1      v_bit 1       duration 5
i 2       page 2      r_bit 1      v_bit 1       duration 4
i 2       page 2      r_bit 1      v_bit 1       duration 3
 *** 6 clock ticks - current r_bit set to 0 *** 
i 3       page 3      r_bit 1      v_bit 1       duration 3
i 3       page 3      r_bit 1      v_bit 1       duration 2
i 3       page 3      r_bit 1      v_bit 1       duration 1
i 4       page 4      r_bit 1      v_bit 1       duration 9
i 4       page 4      r_bit 1      v_bit 1       duration 8
i 4       page 4      r_bit 1      v_bit 1       duration 7
 *** 6 clock ticks - current r_bit set to 0 *** 
i 5       page 0      r_bit 0      v_bit 1       duration 1
Fault: page 0 evicted, 5 brought into memory.
i 6       page 1      r_bit 0      v_bit 0       duration 0
i 7       page 2      r_bit 0      v_bit 1       duration 2
Fault: page 0 evicted, 7 brought into memory.
i 7       page 2      r_bit 1      v_bit 1       duration 1
i 8       page 3      r_bit 1      v_bit 1       duration 0
i 9       page 4      r_bit 0      v_bit 1       duration 6
Fault: page 0 evicted, 9 brought into memory.
i 9       page 4      r_bit 1      v_bit 1       duration 5
i 9       page 4      r_bit 1      v_bit 1       duration 4
 *** 6 clock ticks - current r_bit set to 0 *** 
i 10       page 0      r_bit 1      v_bit 0       duration 0
i 11       page 1      r_bit 0      v_bit 0       duration 0
i 12       page 2      r_bit 1      v_bit 1       duration 0
i 13       page 3      r_bit 1      v_bit 1       duration 0
i 14       page 4      r_bit 0      v_bit 1       duration 3
Fault: page 0 evicted, 14 brought into memory.
i 14       page 4      r_bit 1      v_bit 1       duration 2
i 14       page 4      r_bit 1      v_bit 1       duration 1
i 15       page 0      r_bit 1      v_bit 0       duration 0
i 16       page 1      r_bit 0      v_bit 0       duration 0
i 17       page 2      r_bit 1      v_bit 1       duration 0
i 18       page 3      r_bit 1      v_bit 1       duration 0
i 19       page 4      r_bit 1      v_bit 1       duration 0
i 20       page 0      r_bit 1      v_bit 0       duration 0
i 21       page 1      r_bit 0      v_bit 0       duration 0
i 22       page 2      r_bit 1      v_bit 1       duration 0
i 23       page 3      r_bit 1      v_bit 1       duration 0
i 24       page 4      r_bit 1      v_bit 1       duration 0

Total number of faults is 4


'''

