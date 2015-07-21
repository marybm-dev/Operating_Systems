# Mary Martinez
# Created on 7/14/15
# 
# cup_scheduling.py
# Python implementation of CPU Scheduling
# First Come First Serve (FCFS) vs. Round Robin (RR)
# 

from collections import deque
from recordclass import recordclass
from random import randint

JobStruct = recordclass("JobStruct", "time_arrival time_required")

def generate_jobs(n):
	jobs = []
	total_time = 0
	# randomly generate jobs
	for i in range(n):
		arrived = i
		required = randint(0, 40) + 2
		total_time += required
		jobs.append(JobStruct(time_arrival = arrived, time_required = required))
		print "Job <", arrived, ",", required, ">"

	print "Average Job Time: ",total_time/len(jobs)

	# return the array
	return jobs

class FCFS(object):
	def __init__(self):
		super(FCFS, self).__init__()

	def process_jobs(self, jobs_array):
		total_jobs = len(jobs_array)
		total_time = 0
		cpu_cycles = 0

		# add up the cycles and time to complete jobs
		for job in jobs_array:
			total_time = total_time + job.time_required
			cpu_cycles += 1

		# the avg time for each job and throughput are the same for FCFS because there's not preemptive
		avg_job_time = total_time/total_jobs

		print "FCFS Processing Time: ", total_time,"ms [cpu cycles:",cpu_cycles,"] [avg throughput:",avg_job_time,"ms ]"

class RR(object):
	def __init__(self):
		super(RR, self).__init__()

	def process_jobs(self, jobs_array):
		total_jobs = len(jobs_array)
		total_time = 0
		rr_time = 0
		cpu_cycles = 0
		context_switching = randint(2,10)
		quantum = randint(2,20)

		# add jobs into circular q
		circular_queue = deque(maxlen = len(jobs_array))
		for job in jobs_array:
			circular_queue.append(job)
			total_time += job.time_required

		# continue until all jobs processed
		while True:

			for job in list(circular_queue):
				# only add the quantum and context switching if there is >1 jobs
				if len(circular_queue) > 1:
					rr_time += (quantum + context_switching)
				else:
					rr_time += quantum
				
				# reduce the amount of time left for this job to complete
				job.time_required -= quantum
				cpu_cycles += 1
				
				# check if the job is complete, pop from queue if so
				if job.time_required < 0:
					circular_queue.pop()

			# exit the while loop once the queue is empty
			if len(circular_queue) == 0:
				break

		# get the avg job throughput
		avg_job_through = rr_time/total_jobs

		# get the avg time for each job
		avg_job_time = total_time/total_jobs

		print "RR Processing Time: ", rr_time,"ms [cpu cycles:",cpu_cycles,"] [avg throughput:",avg_job_through,"ms ] [context switching:",context_switching,"ms] [quantum:",quantum,"ms]"


# run the simulation
random_jobs = generate_jobs(randint(1, 20))
fcfc_process = FCFS()
fcfc_process.process_jobs(random_jobs)
rr_process = RR()
rr_process.process_jobs(random_jobs)


### Analysis of results
# I compared the algorithms First Come First Serve and Round Robin
# First Come First Serve processes jobs as they come in, priority given in the sequential order that jobs arrive in
# Round Robin adds jobs into a circular queue and processes a quantum amount of time and moves to the next job after quantum time
# The out put shows that FCFS always performed faster. This is because the Round Robin algorithm stops the processing and there is 
# overhead to stop one job, move to the next, stop one job, move to the next, etc. In the case of FCFS the jobs are processed until complete.
# Below I have included the output of 5 different run time results. All processes were randomly generated and vary in size.
# The resulsts clearly demonstrate the overhead needed when comparing the amount of processing time using both algorithms.
# Also it is good to note the varying quantum sizes and context switching - however, in my case the FCFS always beat RR.

### runtime results 1
# Job < 0 , 31 >
# Job < 1 , 24 >
# Average Job Time:  27
# FCFS Processing Time:  55 ms [cpu cycles: 2 ] [avg throughput: 27 ms ]
# RR Processing Time:  103 ms [cpu cycles: 9 ] [avg throughput: 51 ms ] [context switching: 5 ms] [quantum: 7 ms]

### runtime results 2
# Job < 0 , 9 >
# Job < 1 , 42 >
# Job < 2 , 39 >
# Job < 3 , 17 >
# Job < 4 , 5 >
# Job < 5 , 33 >
# Job < 6 , 9 >
# Job < 7 , 22 >
# Job < 8 , 31 >
# Job < 9 , 22 >
# Job < 10 , 31 >
# Job < 11 , 4 >
# Job < 12 , 15 >
# Job < 13 , 32 >
# Job < 14 , 25 >
# Job < 15 , 28 >
# Job < 16 , 32 >
# Job < 17 , 2 >
# Job < 18 , 16 >
# Average Job Time:  21
# FCFS Processing Time:  414 ms [cpu cycles: 19 ] [avg throughput: 21 ms ]
# RR Processing Time:  770 ms [cpu cycles: 31 ] [avg throughput: 40 ms ] [context switching: 5 ms] [quantum: 20 ms]

### runtime results 3
# Job < 0 , 12 >
# Job < 1 , 24 >
# Job < 2 , 7 >
# Job < 3 , 18 >
# Job < 4 , 41 >
# Job < 5 , 42 >
# Job < 6 , 41 >
# Average Job Time:  26
# FCFS Processing Time:  185 ms [cpu cycles: 7 ] [avg throughput: 26 ms ]
# RR Processing Time:  213 ms [cpu cycles: 36 ] [avg throughput: 30 ms ] [context switching: 3 ms] [quantum: 3 ms]

### runtime results 4
# Job < 0 , 19 >
# Job < 1 , 6 >
# Job < 2 , 8 >
# Job < 3 , 17 >
# Job < 4 , 26 >
# Job < 5 , 18 >
# Job < 6 , 9 >
# Job < 7 , 36 >
# Job < 8 , 7 >
# Job < 9 , 11 >
# Job < 10 , 38 >
# Job < 11 , 23 >
# Job < 12 , 35 >
# Job < 13 , 13 >
# Job < 14 , 19 >
# Job < 15 , 16 >
# Job < 16 , 27 >
# Job < 17 , 9 >
# Average Job Time:  18
# FCFS Processing Time:  337 ms [cpu cycles: 18 ] [avg throughput: 18 ms ]
# RR Processing Time:  823 ms [cpu cycles: 49 ] [avg throughput: 45 ms ] [context switching: 10 ms] [quantum: 7 ms]

### runtime results 5
# Job < 0 , 28 >
# Job < 1 , 2 >
# Job < 2 , 15 >
# Job < 3 , 34 >
# Job < 4 , 22 >
# Job < 5 , 20 >
# Job < 6 , 7 >
# Job < 7 , 13 >
# Job < 8 , 30 >
# Job < 9 , 13 >
# Job < 10 , 24 >
# Job < 11 , 17 >
# Job < 12 , 12 >
# Job < 13 , 30 >
# Job < 14 , 15 >
# Average Job Time:  18
# FCFS Processing Time:  282 ms [cpu cycles: 15 ] [avg throughput: 18 ms ]
# RR Processing Time:  522 ms [cpu cycles: 22 ] [avg throughput: 34 ms ] [context switching: 6 ms] [quantum: 18 ms]