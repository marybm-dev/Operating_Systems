'''
Maria Martinez
CS 4560 - Operating Systems (Summer '15)
Assignment 04 - Deadlock Avoidance

Purpose: Simulate deadlock avoidance. Two students ask the professor questions.
		 Student can't ask until professor is done answering.
'''

import multiprocessing
import threading
import time
import logging

logging.basicConfig(level=logging.DEBUG, format='(%(threadName)-10s) %(message)s',)

def student(cond):
    cond.acquire()
    question_start(cond)
    question_done(cond)
    cond.release()

def professor(cond):
    cond.acquire()
    while True:
        answer_start()
        answer_done(cond)
        cond.wait()
    cond.release()

def answer_start():
    logging.debug('Answer begin')

def answer_done(cond):
    logging.debug('Answer done')
    cond.notify()							# let the student know the answer is complete so question can be done

def question_start(cond):
    logging.debug('Question begin')
    cond.notify()							# notify the professor so they can answer the question

def question_done(cond):
    cond.wait()								# wait for the professor's answer before the question can be done
    logging.debug('Question done')

if __name__ == '__main__':
    condition = threading.Condition()
    
    p = threading.Thread(name='professor', target=professor, args=(condition,))
    s1 = threading.Thread(name='student1', target=student, args=(condition,))
    s2 = threading.Thread(name='student2', target=student, args=(condition,))

    s1.start()
    p.start()
    s2.start()

    s1.join()
    p.join()
    s2.join()

# sample output:
# (student1  ) Question begin
# (professor ) Answer begin
# (professor ) Answer done
# (student1  ) Question done
# (student2  ) Question begin
# (professor ) Answer begin
# (professor ) Answer done
# (student2  ) Question done