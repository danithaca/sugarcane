#! /usr/bin/env python
import math, random, time, subprocess, datetime
import Queue
import multiprocessing as mp

### Global variables ##########################################################

blog_path = '/scratch/unmirrored2/agong/blog_crawl_2012-01/'
blog_mirror_path = blog_path+'mirrors/'
blog_log_path = blog_path+'logs/'

pending_log = 'logs/pending.txt'
complete_log = 'logs/complete.txt'
num_workers = 15
 
###############################################################################

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

    def shillyShally(self, job):
        time.sleep(float(random.uniform(.1,3)))
        return ( "A", "Z" )
                   
    def getBlog(self, blog_url):
        #	command_string = 'wget -mk http://'+site_url+' -w 5 -t 3 -T 30 -P '+blog_mirror_path
        #	command_string = command_string.split(' ')
        #	p = subprocess.Popen( command_string )
        #	p.wait()

        log_file = blog_log_path + site_url + '.log'
        command_string = 'wget -mk http://'+site_url+' -w 5 -t 3 -T 30 -l 1 -P '+blog_mirror_path+' -o '+log_file
        p = subprocess.Popen( ["-c", command_string], shell=True )
        p.wait()
        return (blog_mirror_path+'/'+blog_url, log_file)
 
    def run(self):
        while not self.kill_received: 
            # get a task
            try:
                job = self.work_queue.get_nowait()
            except Queue.Empty:
                #I'm quitting -- remove me from the active count
                self.active_workers.value -= 1
                break
 
            #Punch in
            start_time = datetime.datetime.now()
            self.log_queue.put({"status":"Start","info":{
                "blog_url" : job,
                "start_time" : start_time.strftime("%Y-%m-%d %H:%M:%S"),
            }})
            
            # the actual processing
            (file_path, log_file) = self.shillyShally(job)
            #(file_path, log_file) = self.getBlog(job)
 
            #Punch out
            end_time = datetime.datetime.now()
            self.log_queue.put({"status":"Done","info":{
                "blog_url" : job,
                "file_path" : file_path,
                "log_file" : log_file,
                "start_time" : start_time.strftime("%Y-%m-%d %H:%M:%S"),
                "end_time" : end_time.strftime("%Y-%m-%d %H:%M:%S"),
            }})

class LogWorker(mp.Process):
    def __init__(self, log_queue, active_workers):
        # base class initialization
        mp.Process.__init__(self)
 
        # job management stuff
        self.log_queue = log_queue
        self.kill_received = False
        self.active_workers = active_workers
        
    def rewritePendingLog(self, pending):
        p_log = file(pending_log,'w')
        for p in pending:
            p_log.write( p + '\t' + pending[p] + '\n' )
        p_log.close()
 
    def run(self):
        pending = {}#'placeholder' : ''}
        time_to_quit = False
        
        while not self.kill_received:
            # get a task
            try:
                message = self.log_queue.get_nowait()
                time_to_quit = False

                #Store to log
                url = message["info"]["blog_url"]
                start_time = message["info"]["start_time"]

                if message["status"] == "Start":
                    pending[url] = start_time
                    self.rewritePendingLog( pending )
                
                elif message["status"] == "Done":
                    del pending[url]
                    self.rewritePendingLog( pending )
                    
                    fields = ["blog_url","start_time","end_time","file_path","log_file"]
                    out_log = file(complete_log,'a').write( '\t'.join( [ message["info"][f] for f in fields ] ) + '\n' )
            
            except Queue.Empty:
                if time_to_quit:
                    break

                time.sleep(0.10)
                if self.active_workers.value == 0:
                    time_to_quit = True
                

##############################################################################


#generate jobs
#blog_urls = 

#jobs = [{
#    "blog_url":str(random.uniform(.1,3)),
#    "delay":random.uniform(.1,3)
#} for a in range(200) ]
jobs = [ str(a) for a in range(200) ]

# load up work queue
work_queue = mp.Queue()
for job in jobs:
    work_queue.put(job)

# create a queue to pass to workers to handling logging
log_queue = mp.Queue()

active_workers = mp.Value('d')

# spawn blog workers
for i in range(num_workers):
    worker = BlogWorker(work_queue, log_queue, active_workers)
    worker.start()

# spawn log worker
log_worker = LogWorker(log_queue, active_workers)
log_worker.start()

