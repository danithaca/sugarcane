#! /usr/bin/env python
import math, random, time, subprocess
import Queue
import multiprocessing as mp
 
#from /users/agong/my_stuff/my_projects/unfinished/iPhD/panel_crawl

def getSite( site_url ):
	command_string = 'wget -mk http://'+site_url+' -w 5 -t 3 -T 30 -P /scratch/unmirrored5/agong/blog_panel_crawl'
	command_string = command_string.split(' ')
	p = subprocess.Popen( command_string )
	p.wait()


def shillyShally( delay ):
    time.sleep(float(delay))


class BlogWorker(mp.Process):
    def __init__(self, work_queue, log_queue, active_workers):
        # base class initialization
        mp.Process.__init__(self)
 
        # job management stuff
        self.work_queue = work_queue
        self.log_queue = log_queue
        self.kill_received = False
        self.active_workers = active_workers

        #Count me as active!
        self.active_workers.value += 1
 
    def run(self):
        while not self.kill_received: 
            # get a task
            try:
                job = self.work_queue.get_nowait()
            except Queue.Empty:
                #I'm quitting -- remove me from the active count
                self.active_workers.value -= 1
                break
 
            #Log the start
            self.log_queue.put({"status":"Start","info":job})
            
            # the actual processing
            shillyShally(job)
 
            # store the result
            self.log_queue.put({"status":"Done","info":job})

class LogWorker(mp.Process):
    def __init__(self, log_queue, active_workers):
        # base class initialization
        mp.Process.__init__(self)
 
        # job management stuff
        self.log_queue = log_queue
        self.kill_received = False
        self.active_workers = active_workers
 
    def run(self):
        while not self.kill_received:
            # get a task
            try:
                message = self.log_queue.get_nowait()

                #Store to log
                if message["status"] == "Start":
                    print "Starting", message["info"], self.active_workers.value
                    pass
                
                elif message["status"] == "Done":
                    print "Done", message["info"], self.active_workers.value
                    pass
                
                else:
                    print "Warning  : unrecognized status :", status
            
            except Queue.Empty:
                time.sleep(.5)
                if self.active_workers.value == 0: break


if __name__ == "__main__":
    #generate jobs
    jobs = [ random.randint(1,5) for a in range(20) ]

    # load up work queue
    work_queue = mp.Queue()
    for job in jobs:
        work_queue.put(job)
 
    # create a queue to pass to workers to handling logging
    log_queue = mp.Queue()
 
    active_workers = mp.Value('d', 0)
    
    # spawn blog workers
    for i in range(num_processes):
        worker = BlogWorker(work_queue, log_queue, active_workers)
        worker.start()
    
    log_worker = LogWorker(log_queue, active_workers)
    log_worker.start()

